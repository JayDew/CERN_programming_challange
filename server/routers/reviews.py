from fastapi import APIRouter, Depends

from server.auth import JWTBearer, get_current_user
from server.crud.reviews import get_reviews_by_id, get_average_review, add_review
from server.schemas import Review, ReviewBase
from server.utils import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("/{plate_id}")
async def get_reviews(
        plate_id,
        db_session: Session = Depends(get_db),
        dependencies=Depends(JWTBearer())
):
    """Find orders belonging dish."""
    return get_reviews_by_id(db_session, plate_id)


@router.get("/{plate_id}/average")
async def get_average_reviews(
        plate_id,
        db_session: Session = Depends(get_db),
        dependencies=Depends(JWTBearer())
):
    """Find orders belonging dish."""
    return get_average_review(db_session, plate_id)

@router.post("/add")
async def add_new_review(
        item: ReviewBase,
        db_session: Session = Depends(get_db),
        dependencies=Depends(JWTBearer())
):
    """Add new order from user."""
    user_id = get_current_user(dependencies)
    return add_review(db_session, item, user_id)
