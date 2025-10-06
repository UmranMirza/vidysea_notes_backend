from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from application.configuration.db import Base

primitive = (int, float, str, bool)


def is_primitive(thing):
    return isinstance(thing, primitive)




def serialize(obj, datetime_format=None, with_timestamp=[]):
    if obj is None:
        return None
    if is_primitive(obj):
        return obj
    if isinstance(obj, Decimal):
        return float(str(obj))
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, datetime):
        return obj.isoformat() if not datetime_format else obj.strftime(datetime_format)
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, list):
        return [serialize(v, datetime_format=datetime_format, with_timestamp=with_timestamp) for v in obj]
    if isinstance(obj, dict):
        return {
            k: serialize(v, datetime_format=datetime_format, with_timestamp=with_timestamp) for k, v in obj.items()
        }
    if isinstance(obj,Base):
        return {
                column.key: serialize(getattr(obj, attr), datetime_format=datetime_format, with_timestamp=with_timestamp)
                for attr, column in list(filter(lambda d: d[0] not in list(set(['created_at','updated_at', 'deleted_at'])-set(with_timestamp)), obj.__mapper__.c.items()))
            }
    return {
        k: serialize(v, datetime_format=datetime_format, with_timestamp=with_timestamp)
        for k, v in obj.__dict__.items()
    }


def serialize_cursor_result(cr):
    arr = []
    for r in cr:
        temp_obj = {}
        for key in r.keys():
            temp_obj[key] = serialize(r[key])
        arr.append(temp_obj)
    return arr