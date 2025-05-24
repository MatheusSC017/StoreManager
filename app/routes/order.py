from sqlalchemy.exc import IntegrityError
from app.models.order import Order
from app.schemas.order_schema import OrderCreate, OrderOut, ProductQuantity
from app.controllers.order_controller import create_order, update_order, delete_order, get_order, get_orders
from fastapi import APIRouter, HTTPException, Request
from typing import List
from app.auth.decorators import auth_required

router = APIRouter()


@router.get("/", response_model=List[OrderOut])
@auth_required
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


@router.post("/", response_model=OrderOut)
@auth_required
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


@router.put("/{order_id}", response_model=OrderOut)
@auth_required
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
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error updating order.")


@router.delete("/{order_id}", response_model=dict)
@auth_required
async def delete(request: Request, order_id: int):
    try:
        deleted: bool = delete_order(order_id)
        if deleted:
            return {"detail": "Order deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Error deleting order.")
    except HTTPException as exception:
        raise exception
    except Exception:
        raise HTTPException(status_code=400, detail="Error deleting order.")


@router.get("/{order_id}", response_model=OrderOut)
@auth_required
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
    except Exception:
        raise HTTPException(status_code=400, detail="Error getting order.")
    return response
