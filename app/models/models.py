import bcrypt
from sqlalchemy import TIMESTAMP, Column, Integer, String, DateTime, func
from app.db import Base
from fastapi_utils.guid_type import GUID_DEFAULT_SQLITE
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=GUID_DEFAULT_SQLITE, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())

    def set_password(self, password: str):
        # Implement your password hashing logic here
        password_to_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_to_bytes, salt)
        self.password = hashed