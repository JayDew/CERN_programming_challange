from sqlalchemy.orm import Session
import server.models as md
from sqlalchemy import func
from fastapi import HTTPException

from server.schemas import ReviewBase


def get_reviews_by_id(db_session: Session, plate_id):
    """Return orders belonging to a dish"""
    return (db_session.query(md.Review).join(md.UserReview)
            .filter(md.UserReview.plate_id == plate_id)
            .all())


def get_average_review(db_session: Session, plate_id):
    """Return average rating of a dish"""
    return db_session.query(func.avg(md.Review.rating)).join(md.UserReview) \
        .filter(md.UserReview.plate_id == plate_id).scalar()


def add_review(db_session: Session, item: ReviewBase, user_id: int):
    """Create new order belonging to a user"""
    # Check if rating is from 1 to 5.
    if not 1 <= item.rating <= 5:
        raise HTTPException(
            status_code=400,
            detail="Rating should be from 1 to 5"
        )

    # Check if user already placed a review
    count = (db_session.query(md.UserReview)
             .filter(md.UserReview.user_id == user_id)
             .filter(md.UserReview.plate_id == item.plate_id)
             .count())

    if count >= 1:
        raise HTTPException(
            status_code=404,
            detail="User already placed a rating."
        )

    # Check if user ordered that dish
    ordered = (db_session.query(md.UserOrder)
               .join(md.PlateOrder, md.UserOrder.order_id == md.PlateOrder.order_id)
               .filter(md.UserOrder.user_id == user_id)
               .filter(md.PlateOrder.plate_id == item.plate_id)
               .count())

    if ordered == 0:
        raise HTTPException(
            status_code=404,
            detail="User did not order the dish."
        )

    review = md.Review()
    review.review = item.review
    review.rating = item.rating

    db_session.add(review)
    db_session.commit()
    db_session.refresh(review)

    user_reveiw = md.UserReview()
    user_reveiw.user_id = user_id
    user_reveiw.plate_id = item.plate_id
    user_reveiw.review_id = review.review_id

    db_session.add(user_reveiw)
    db_session.commit()
    db_session.refresh(user_reveiw)
    return review
