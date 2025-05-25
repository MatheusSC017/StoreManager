from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))

    product = relationship("Product", back_populates="images")


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
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
