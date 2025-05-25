from fastapi import HTTPException, UploadFile
from app.models.product import Product, ProductImage
from app.schemas.product_schema import ProductCreate
from app.db.session import SessionLocal
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.core.config import settings
import os, shutil


os.makedirs(settings.STATIC_DIR, exist_ok=True)


def create_product(product_data: ProductCreate, images: Optional[List[UploadFile]] = None) -> Product:
    with SessionLocal() as db:
        product = Product(description=product_data.description, value=product_data.value, barcode=product_data.barcode,
                          section=product_data.section, stock=product_data.stock, expiration_date=product_data.expiration_date)
        db.add(product)
        db.flush()

        if images:
            for image in images:
                filename = f"{product.id}_{image.filename}"
                filepath = os.path.join(settings.STATIC_DIR, filename)

                with open(filepath, "wb") as f:
                    shutil.copyfileobj(image.file, f)

                image_entry = ProductImage(filename=filename, product_id=product.id)
                db.add(image_entry)

        db.commit()
        product_with_images = db.query(Product).options(
            selectinload(Product.images).selectinload(ProductImage.product)
        ).filter(Product.id == product.id).first()

        return product_with_images


def update_product(product_id: int, product_data: ProductCreate, images: Optional[List[UploadFile]] = None) -> Product:
    with SessionLocal() as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.description = product_data.description
        product.value = product_data.value
        product.barcode = product_data.barcode
        product.section = product_data.section
        product.stock = product_data.stock
        product.expiration_date = product_data.expiration_date

        if images:
            for image in images:
                filename = f"{product.id}_{image.filename}"
                filepath = os.path.join(settings.STATIC_DIR, filename)

                with open(filepath, "wb") as f:
                    shutil.copyfileobj(image.file, f)

                image_entry = ProductImage(filename=filename, product_id=product.id)
                db.add(image_entry)

        db.commit()
        product_with_images = db.query(Product).options(
            selectinload(Product.images).selectinload(ProductImage.product)
        ).filter(Product.id == product.id).first()

        return product_with_images


def delete_product(product_id: int) -> bool:
    with SessionLocal() as db:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        for image in product.images:
            filepath = os.path.join(settings.STATIC_DIR, image.filename)
            if image.filename and os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(e)
                    raise HTTPException(status_code=400, detail="Error deleting image")

        db.delete(product)
        db.commit()
        return True


def get_products() -> List[Product]:
    with SessionLocal() as db:
        product = db.query(Product).options(selectinload(Product.images)).all()
        return product


def get_product(product_id: int) -> Product:
    with SessionLocal() as db:
        product = db.query(Product).options(selectinload(Product.images)).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
