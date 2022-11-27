from flask_login import UserMixin
from sqlalchemy import Column, String, BLOB, Boolean
from sqlalchemy.orm import relationship
from .base_model import BaseModel


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    notes = relationship("Note", backref="user")
    profile_image = Column(BLOB)
    is_admin = Column(Boolean, default=False)
