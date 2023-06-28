import bcrypt
import jwt
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from app.models.schemas import UserCreate, UserUpdate, UserLogin
from app.models.models import User

load_dotenv()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    return db_user


def get_user(db: Session, user_id: str):
    data = db.query(User).filter(User.id == user_id).first()
    if data:
        return data
    raise ValueError("User not found")


def update_user(db: Session, user_id: str, user: UserUpdate) -> User:
  db_user = db.query(User).filter(User.id == user_id).first()

  if not db_user:
      raise ValueError("User not found")

  db_user.email = user.email # type: ignore
  db_user.password = user.password # type: ignore
  db_user.username = user.username # type: ignore

  db.commit()
  db.refresh(db_user)
  return db_user


def delete_user(db: Session, user_id: str):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return user

def compare_password(password: str, hashed) -> bool:
    unhashed = password.encode('utf-8')
    thehashed = hashed
    return bcrypt.checkpw(password=unhashed, hashed_password=thehashed)

def login(db: Session, user_data: UserLogin) -> str:
    user = db.query(User).filter(User.username == user_data.username).first()
    if user:
        compare = compare_password(user_data.password, user.password)
        if compare is True:
            user.password = '' # type: ignore
            serialized_data = jsonable_encoder(user)
            jwt_secret = os.getenv('SECRET_KEY')
            encode_jwt = jwt.encode(serialized_data, jwt_secret, algorithm="HS256")
            return encode_jwt
        raise ValueError("Incorrect login details")
    raise ValueError("Incorrect login details")