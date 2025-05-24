from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.schemas.order_schema import ProductQuantity


class OrderProduct(Base):
    __tablename__ = "order_products"

    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)

    client = relationship("Client", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order")
