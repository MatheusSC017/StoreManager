from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from app.db.session import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    barcode = Column(String, unique=True, index=True)
    section = Column(String, index=True)
    stock = Column(Integer, nullable=False)
    expiration_date = Column(Date, nullable=True)

    order_products = relationship("OrderProduct", back_populates="product")
