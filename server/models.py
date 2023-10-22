import random

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    ForeignKey,
    Float,
    String,
    Boolean
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def random_delay():
    delta =  random.randint(60, 900)
    return datetime.now() + timedelta(seconds=delta)


class PlateOrder(Base):
    __tablename__ = 'plate_order'

    plate_id = Column(ForeignKey('plate.plate_id'), primary_key=True)
    order_id = Column(ForeignKey('order.order_id'), primary_key=True)
    quantity = Column(Integer, default=1, nullable=False)
    
    plate = relationship("Plate", back_populates="orders")
    order = relationship("Order", back_populates="plates")


class Plate(Base):
    __tablename__ = "plate"

    plate_id = Column(Integer, primary_key=True)
    plate_name = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    picture = Column(Text)

    orders = relationship("PlateOrder", back_populates="plate")


class Order(Base):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True)
    state = Column(String(50))
    order_time = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    __finish_time = Column(DateTime(timezone=True), default=random_delay, nullable=False)

    plates = relationship("PlateOrder", back_populates="order")

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.now)

class UserOrder(Base):
    __tablename__ = 'user_order'

    user_id = Column(ForeignKey('users.user_id'), primary_key=True)
    order_id = Column(ForeignKey('order.order_id'), primary_key=True)

class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True)
    review = Column(String(800), nullable=False)
    rating = Column(Integer)

class UserReview(Base):
    __tablename__ = 'user_review'

    user_id = Column(ForeignKey('users.user_id'), primary_key=True)
    review_id = Column(ForeignKey('reviews.review_id'), primary_key=True)
    plate_id = Column(ForeignKey('plate.plate_id'), primary_key=True)
