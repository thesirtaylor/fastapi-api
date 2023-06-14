from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.models.schemas import UserCreate, UserUpdate
from app.services.user_service import create_user, get_user, update_user, delete_user
from app.db import get_db
from app.api.util_func import http_exception, success_response


router = APIRouter()

@router.post("/users")
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)) -> Response:
    try:
        created_user = create_user(db, user)
        user_data = {*created_user.username}
        return JSONResponse(content = user_data, status_code=201)
    except Exception as e:
        raise http_exception(500, str(e))


@router.get("/users/{user_id}")
def get_user_endpoint(user_id: str, db: Session = Depends(get_db)):
    try:
        returndata = get_user(db, user_id)
        return JSONResponse(content = returndata, status_code=201)
    except Exception as e:
        raise http_exception(500, str(e))


@router.put("/users/{user_id}")
def update_user_endpoint(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    try:
       returndata = update_user(db, user_id, user)
       return JSONResponse(content = returndata, status_code=201)
    except Exception as e:
        raise http_exception(500, str(e))
    

@router.delete("/users/{user_id}")
def delete_user_endpoint(user_id: str, db: Session = Depends(get_db)):
    try:
       returndata = delete_user(db, user_id)
       return JSONResponse(content = returndata, status_code=201)
    except Exception as e:
        raise http_exception(500, str(e))