from fastapi import HTTPException

from app.models.product import Product
from app.schemas.product_schema import ProductCreate
from app.db.session import SessionLocal
from typing import List


def create_product(product_data: ProductCreate) -> Product:
    with SessionLocal() as db:
        product = Product(description=product_data.description, value=product_data.value, barcode=product_data.barcode,
                          section=product_data.section, stock=product_data.stock, expiration_date=product_data.expiration_date)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product


def update_product(product_id: int, product_data: ProductCreate) -> Product:
    with SessionLocal() as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            db.close()
            raise HTTPException(status_code=404, detail="Product not found")
        product.description = product_data.description
        product.value = product_data.value
        product.barcode = product_data.barcode
        product.section = product_data.section
        product.stock = product_data.stock
        product.expiration_date = product_data.expiration_date

        db.commit()
        db.refresh(product)
        return product


def delete_product(product_id: int) -> bool:
    with SessionLocal() as db:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            db.close()
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete(product)
        db.commit()
        return True


def get_products() -> List[Product]:
    with SessionLocal() as db:
        product = db.query(Product).all()
        return product


def get_product(product_id: int) -> Product:
    with SessionLocal() as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
