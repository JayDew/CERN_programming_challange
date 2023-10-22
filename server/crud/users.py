from jose import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import status

from server.auth import get_hashed_password, verify_password, create_access_token, create_refresh_token, JWT_SECRET_KEY, \
    ALGORITHM
from server.schemas import requestdetails, ChangePassword

import server.models as md


def create_user(session: Session, user):
    """Create a new user"""
    existing_user = session.query(md.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)

    new_user = md.User(username=user.username, email=user.email, password=encrypted_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "user created successfully"}


def user_login(db: Session, request: requestdetails):
    """Hand out jwt token for authenticated user"""
    user = db.query(md.User).filter(md.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    access = create_access_token(user.user_id)
    refresh = create_refresh_token(user.user_id)

    token_db = md.TokenTable(user_id=user.user_id, access_toke=access, refresh_toke=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


def user_change_password(db: Session, request: ChangePassword):
    """Modify user password"""
    user = db.query(md.User).filter(md.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()

    return {"message": "Password changed successfully"}


def user_logout(db: Session, dependencies):
    """Remove auth token from database"""
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    db.query(md.TokenTable).where(md.TokenTable.user_id.in_([user_id])).delete()
    db.commit()
    return {"message": "Logout Successfully"}
