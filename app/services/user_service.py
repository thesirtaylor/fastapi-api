from sqlalchemy.orm import Session

from app.models.schemas import UserCreate, UserUpdate
from app.models.models import User


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

  db_user.email = user.email
  db_user.password = user.password
  db_user.username = user.username

  db.commit()
  db.refresh(db_user)
  return db_user


def delete_user(db: Session, user_id: str):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return user
