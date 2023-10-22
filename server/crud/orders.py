from sqlalchemy.orm import Session
from fastapi import HTTPException
from server.schemas import OrderBase, OrderChangeState

import server.models as md


def get_orders(db_session: Session, user_id):
    """Return orders belonging to a user"""
    return (db_session.query(md.Order).join(md.UserOrder)
            .filter(md.UserOrder.user_id == user_id)
            .all())


def add_order(db_session: Session, item: OrderBase, user_id: int):
    """Create new order belonging to a user"""
    # Check if all plates exist.
    plate_ids = [plate.plate_id for plate in item.plates]
    plate_ids_result = db_session.query(md.Plate.plate_id).filter(
        md.Plate.plate_id.in_(plate_ids)
    )
    if plate_ids_result.count() != len(plate_ids):
        raise HTTPException(
            status_code=404,
            detail="Plate does not exist."
        )

    # Check if quantity of each plate is non-negative.
    for plate in item.plates:
        if plate.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Non-positive plate quantity."
            )

    order = md.Order()
    # Add PlateOrder objects.
    for plate in item.plates:
        plate_order = md.PlateOrder(
            plate_id=plate.plate_id,
            order_id=order.order_id,
            quantity=plate.quantity
        )
        order.plates.append(plate_order)

    order.state = 'SUBMITTED' # initial state
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    #save the user giving the order
    user_order = md.UserOrder()
    user_order.order_id = order.order_id
    user_order.user_id = user_id
    db_session.add(user_order)
    db_session.commit()

    return order


def state_change(current_state, transition):

    if transition == 'REJECT':
        if current_state == 'SUBMITTED':
            return 'REJECTED'
        else:
            return current_state

    if transition == "CANCEL":
        if current_state == "SUBMITTED" or current_state == "APPROVED":
            return "CANCELLED"
        else:
            return current_state

    if transition == "APPROVE":
        if current_state == "SUBMITTED":
            return "APPROVED"
        else:
            return current_state

    if transition == "PREPARE":
        if current_state == "APPROVED":
            return "IN PREPARATION"
        else:
            return current_state

    if transition == "SERVE":
        if current_state == "IN PREPARATION":
            return "IN DELIVERY"
        else:
            return current_state

    if transition == "DELIVER":
        if current_state == "IN DELIVERY":
            return "DELIVERED"
        else:
            return current_state

    return current_state


def change_status(db_session: Session, item: OrderChangeState, user_id: int):
    # get the order
    current_order = (db_session.query(md.Order).join(md.UserOrder)).filter(md.UserOrder.user_id == user_id).filter(
        md.Order.order_id == item.order_id).first()

    if not current_order:
        # if order does not exist
        raise HTTPException(
            status_code=400,
            detail="Order does not exist."
        )

    # get current state
    current_state = current_order.state

    # transition to a new state
    new_state = state_change(current_state, item.transition)

    current_order.state = new_state
    db_session.add(current_order)
    db_session.commit()
    # if save to db
    return current_order
