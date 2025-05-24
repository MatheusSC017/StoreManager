from fastapi import HTTPException
from app.models.order import Order, OrderProduct
from app.models.product import Product
from app.models.client import Client
from app.schemas.order_schema import OrderCreate
from app.db.session import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from typing import List


def create_order(order_data: OrderCreate) -> Order:
    with SessionLocal() as db:
        try:
            client = db.query(Client).filter(Client.id == order_data.client_id).first()
            if not client:
                raise HTTPException(status_code=404, detail=f"Client {order_data.client_id} not found")

            order = Order(client_id=order_data.client_id, date=order_data.date, status=order_data.status)
            db.add(order)
            db.flush()

            for order_product in order_data.products:
                product = db.query(Product).filter(Product.id == order_product.product_id).first()
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product {order_product.product_id} not found")
                if product.stock < order_product.quantity:
                    raise HTTPException(status_code=400, detail="Product without stock requested")
                product.stock -= order_product.quantity

                order_product = OrderProduct(
                    order_id=order.id,
                    product_id=order_product.product_id,
                    quantity=order_product.quantity
                )
                db.add(order_product)

            db.commit()

            order_with_relationships = db.query(Order).options(
                selectinload(Order.order_products).selectinload(OrderProduct.product)
            ).filter(Order.id == order.id).first()

            return order_with_relationships
        except SQLAlchemyError:
            db.rollback()
            raise


def update_order(order_id: int, order_data: OrderCreate) -> Order:
    with SessionLocal() as db:
        try:
            order = db.query(Order).options(selectinload(Order.order_products)).filter(Order.id == order_id).first()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
            order.client_id = order_data.client_id
            order.date = order_data.date
            order.status = order_data.status

            actual_order_products = {item.product_id: item for item in order.order_products}
            new_order_products = {item.product_id: item for item in order_data.products}

            for product_id, item in new_order_products.items():
                product = db.query(Product).filter(Product.id == product_id).first()
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

                if product_id in actual_order_products:
                    order_product = actual_order_products[product_id]
                    diff_quantity = item.quantity - order_product.quantity
                    if product.stock < diff_quantity:
                        raise HTTPException(status_code=400, detail=f"Not enough stock for product {product_id}")
                    product.stock -= diff_quantity
                    order_product.quantity = item.quantity
                else:
                    if product.stock < item.quantity:
                        raise HTTPException(status_code=400, detail=f"Not enough stock for product {product_id}")
                    product.stock -= item.quantity
                    new_order_product = OrderProduct(
                        order_id=order.id,
                        product_id=product_id,
                        quantity=item.quantity
                    )
                    db.add(new_order_product)

            for product_id, order_product in actual_order_products.items():
                if product_id not in new_order_products:
                    product = db.query(Product).filter(Product.id == product_id).first()
                    product.stock += order_product.quantity
                    db.delete(order_product)

            db.commit()

            order_with_relationships = db.query(Order).options(
                selectinload(Order.order_products).selectinload(OrderProduct.product)
            ).filter(Order.id == order.id).first()

            return order_with_relationships
        except SQLAlchemyError:
            db.rollback()
            raise


def delete_order(order_id: int) -> bool:
    with SessionLocal() as db:
        try:
            order = db.query(Order).options(selectinload(Order.order_products)).filter(Order.id == order_id).first()

            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            for order_product in order.order_products:
                product = db.query(Product).filter(Product.id == order_product.product_id).first()
                product.stock += order_product.quantity
                db.delete(order_product)

            db.delete(order)
            db.commit()
            return True
        except SQLAlchemyError:
            db.rollback()
            raise


def get_orders() -> List[Order]:
    with SessionLocal() as db:
        return db.query(Order).options(selectinload(Order.order_products)).all()


def get_order(order_id: int) -> Order:
    with SessionLocal() as db:
        order = db.query(Order).options(selectinload(Order.order_products)).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
