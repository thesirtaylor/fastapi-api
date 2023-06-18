import bcrypt
from sqlalchemy import Column, String, DateTime, func
from app.db import Base
import uuid

def new_uuid():
    x = str(uuid.uuid4())
    return x

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=new_uuid, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())

    def set_password(self, password: str):
        password_to_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_to_bytes, salt)
        self.password = hashed