from datetime import datetime, timedelta
from sqlalchemy import Column,Integer,DateTime
from application import Base
from fastapi_mail import MessageSchema, MessageType

class Generic(Base):
    __abstract__ = True
    id = Column("id", Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deleted_at = Column(DateTime, default=None)

    def save(obj,db):
        db.add(obj)
        db.commit()
        # db.refresh(obj)
        

    def bulk_save_object(obj,db):
        db.bulk_save_objects(obj)
        db.commit()
 
    def delete(obj,db):
        obj.deleted_at = datetime.utcnow()
        db.add(obj)
        db.commit()
        
            
    @classmethod
    def get_by_id(cls, db, id, deleted=False):
        if deleted == False:
            return db.query(cls).filter(cls.deleted_at.is_(None)).filter(cls.id==id).first()
        else:
            return db.query(cls).filter(cls.id==id).first()

    @classmethod
    def get_by_ids(cls, db, ids, deleted=False):
        if deleted == False:
            return db.query(cls).filter(cls.deleted_at.is_(None)).filter(cls.id.in_(ids)).all()
        else:
            return db.query(cls).filter(cls.id.in_(ids)).first()

