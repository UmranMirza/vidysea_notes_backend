from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from application.models.generic import Generic

class User(Generic):
    __tablename__ = "users"
    name = Column(String(128), nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    phone = Column(String(13))
    hashed_password = Column(String(256), nullable=False)
    role = Column(String(32), default="user")  # 'admin' or 'user'
    is_active = Column(Boolean, default=True)

    notes = relationship("Note", back_populates="owner")


