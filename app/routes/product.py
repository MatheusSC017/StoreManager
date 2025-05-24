from sqlalchemy.exc import IntegrityError
from app.models.product import Product
from app.auth.authentication import auth_required
from app.schemas.product_schema import ProductCreate, ProductOut
from app.controllers.product_controller import create_product, update_product, delete_product, get_product, get_products
from fastapi import Depends, APIRouter, HTTPException, Request
from typing import List

router = APIRouter()


@router.get("/", dependencies=[Depends(auth_required)], response_model=List[ProductOut], description="Retrieve all products in stock.")
async def get_all(request: Request):
    products: List[Product] = get_products()
    response = []
    for product in products:
        response.append(ProductOut.from_orm(product))
    return response


@router.post("/", dependencies=[Depends(auth_required)], response_model=ProductOut, description="Add a new product to inventory.")
async def create(request: Request, product_data: ProductCreate):
    try:
        product: Product = create_product(product_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Barcode already in use.")
    return ProductOut.from_orm(product)


@router.put("/{product_id}", dependencies=[Depends(auth_required)], response_model=ProductOut, description="Update product information.")
async def update(request: Request, product_id: int, product_data: ProductCreate):
    try:
        product: Product = update_product(product_id, product_data)
        return ProductOut.from_orm(product)
    except HTTPException as exception:
        raise exception


@router.delete("/{product_id}", dependencies=[Depends(auth_required)], response_model=dict, description="Remove a product from inventory.")
async def delete(request: Request, product_id: int):
    try:
        deleted: bool = delete_product(product_id)
        if deleted:
            return {"detail": "Product deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Error deleting product.")
    except HTTPException as exception:
        raise exception


@router.get("/{product_id}", dependencies=[Depends(auth_required)], response_model=ProductOut, description="View product details.")
async def get(request: Request, product_id: int):
    try:
        product: Product = get_product(product_id)
    except HTTPException as exception:
        raise exception
    return ProductOut.from_orm(product)
