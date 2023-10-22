from fastapi import APIRouter, Depends

from server.crud.users import create_user, user_login, user_change_password, user_logout
from server.schemas import UserCreate, requestdetails, TokenSchema, ChangePassword
from server.utils import get_db
from sqlalchemy.orm import Session

from server.auth import JWTBearer

router = APIRouter()


@router.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_db)):
    return create_user(session, user)


@router.post('/login', response_model=TokenSchema)
def login(request: requestdetails, session: Session = Depends(get_db)):
    return user_login(session, request)


@router.post('/change-password')
def change_password(request: ChangePassword, db: Session = Depends(get_db)):
    return user_change_password(db, request)


@router.post('/logout')
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    return user_logout(db, dependencies)
