from sqlalchemy.exc import IntegrityError
from app.models.order import Order
from app.auth.authentication import auth_required
from app.schemas.order_schema import OrderCreate, OrderOut, ProductQuantity
from app.controllers.order_controller import create_order, update_order, delete_order, get_order, get_orders
from fastapi import Depends, APIRouter, HTTPException, Request
from typing import List

router = APIRouter()


@router.get("/", dependencies=[Depends(auth_required)], response_model=List[OrderOut], description="List all sales orders.")
async def get_all(request: Request):
    orders: List[Order] = get_orders()
    response: List[OrderOut] = []
    for order in orders:
        response.append(OrderOut(
            id=order.id,
            client_id=order.client_id,
            date=order.date,
            status=order.status,
            products=[
                ProductQuantity(product_id=item.product_id, quantity=item.quantity) for item in order.order_products
            ]
        ))
    return response


@router.post("/", dependencies=[Depends(auth_required)], response_model=OrderOut, description="Register a new order (stock is automatically updated).")
async def create(request: Request, order_data: OrderCreate):
    try:
        order: Order = create_order(order_data)
        response: OrderOut = OrderOut(
            id=order.id,
            client_id=order.client_id,
            date=order.date,
            status=order.status,
            products=[
                ProductQuantity(product_id=item.product_id, quantity=item.quantity) for item in order.order_products
            ]
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Barcode already in use.")
    except HTTPException as exception:
        raise exception
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Failed to register order.")
    return response


@router.put("/{order_id}", dependencies=[Depends(auth_required)], response_model=OrderOut, description="Modify an existing order.")
async def update(request: Request, order_id: int, order_data: OrderCreate):
    try:
        order: Order = update_order(order_id, order_data)
        return OrderOut(
            id=order.id,
            client_id=order.client_id,
            date=order.date,
            status=order.status,
            products=[
                ProductQuantity(product_id=item.product_id, quantity=item.quantity) for item in order.order_products
            ]
        )
    except HTTPException as exception:
        raise exception


@router.delete("/{order_id}", dependencies=[Depends(auth_required)], response_model=dict, description="Cancel an order (automatically restore stock).")
async def delete(request: Request, order_id: int):
    try:
        deleted: bool = delete_order(order_id)
        if deleted:
            return {"detail": "Order deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Error deleting order.")
    except HTTPException as exception:
        raise exception


@router.get("/{order_id}", dependencies=[Depends(auth_required)], response_model=OrderOut, description="View details of a specific order.")
async def get(request: Request, order_id: int):
    try:
        order: Order = get_order(order_id)
        response: OrderOut = OrderOut(
            id=order.id,
            client_id=order.client_id,
            date=order.date,
            status=order.status,
            products=[
                ProductQuantity(product_id=item.product_id, quantity=item.quantity) for item in order.order_products
            ]
        )
    except HTTPException as exception:
        raise exception
    return response
