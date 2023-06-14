import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.schemas import UserCreate, UserUpdate
from app.services.user_service import create_user, get_user, update_user, delete_user
from app.db import Base
from main import app



SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
email = "testuser@example.com"
username="testuser"
password="testpassword"

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client


def test_create_user(db):
    user = create_user(db, user = UserCreate(username=username, email=email, password=password))
    assert user.username == "testuser"
    assert user.email == email


def test_get_user(db):
    user = create_user(db, user = UserCreate(username="firsttestcase", email="firsttestemail@email.com", password=password))
    retrieved_user = get_user(db, user_id=str(user.id))
    assert retrieved_user.id == user.id
    assert retrieved_user.username == "firsttestcase"
    assert retrieved_user.email == "firsttestemail@email.com"


def test_update_user(db):
    user = create_user(db, user=UserCreate(username="secondtestcase", email="secondtestemail@email.com", password=password))
    oldemail = user.email
    oldusername = user.username
    updated_user = update_user(db, user_id=str(user.id), user = UserUpdate(username="updateduser", email="secondtestemail@example.com", password="thenewPassword"))
    print(updated_user.email, updated_user.username, updated_user.password)
    assert updated_user.username == "updateduser"
    assert oldemail != updated_user.email
    assert oldusername != updated_user.username
    assert updated_user.email == "secondtestemail@example.com"


def test_delete_user(db):
    user = create_user(db, user=UserCreate(username="thirdtestcase", email="thirdtestemail@gemail.com", password=password))
    delete_user(db, user_id=str(user.id))
    with pytest.raises(ValueError):
        assert get_user(db, user_id=str(user.id))
