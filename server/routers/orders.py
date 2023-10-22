from fastapi import APIRouter, Depends

from server.auth import JWTBearer, get_current_user
from server.schemas import OrderBase, Order, OrderChangeState
from server.crud.orders import get_orders, add_order, change_status
from server.utils import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("", response_model=List[Order])
async def search_orders(
        db_session: Session = Depends(get_db),
        dependencies=Depends(JWTBearer())
):
    """Find orders belonging to user."""
    user_id = get_current_user(dependencies)
    return get_orders(db_session, user_id)


@router.post("", response_model=Order)
async def add_new_order(
        item: OrderBase,
        db_session: Session = Depends(get_db),
        dependencies=Depends(JWTBearer())
):
    """Add new order from user."""
    user_id = get_current_user(dependencies)
    return add_order(db_session, item, user_id)


@router.post("/change-state", response_model=Order)
async def change_order_state(
        item: OrderChangeState,
        db_session: Session = Depends(get_db),
        dependencies=Depends(JWTBearer())
):
    """Change the status of an order"""
    user_id = get_current_user(dependencies)
    return change_status(db_session, item, user_id)
