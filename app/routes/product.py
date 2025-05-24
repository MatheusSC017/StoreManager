from sqlalchemy.exc import IntegrityError
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductOut
from app.controllers.product_controller import create_product, update_product, delete_product, get_product, get_products
from fastapi import APIRouter, HTTPException, Request
from typing import List
from app.auth.decorators import auth_required

router = APIRouter()


@router.get("/", response_model=List[ProductOut])
@auth_required
async def get_all(request: Request):
    products: List[Product] = get_products()
    response = []
    for product in products:
        response.append(ProductOut.from_orm(product))
    return response


@router.post("/", response_model=ProductOut)
@auth_required
async def create(request: Request, product_data: ProductCreate):
    try:
        product: Product = create_product(product_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Barcode already in use.")
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to register product.")
    return ProductOut.from_orm(product)


@router.put("/{product_id}", response_model=ProductOut)
@auth_required
async def update(request: Request, product_id: int, product_data: ProductCreate):
    try:
        product: Product = update_product(product_id, product_data)
        return ProductOut.from_orm(product)
    except HTTPException as exception:
        raise exception
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error updating product.")


@router.delete("/{product_id}", response_model=dict)
@auth_required
async def delete(request: Request, product_id: int):
    try:
        deleted: bool = delete_product(product_id)
        if deleted:
            return {"detail": "Product deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Error deleting product.")
    except HTTPException as exception:
        raise exception
    except Exception:
        raise HTTPException(status_code=400, detail="Error deleting product.")


@router.get("/{product_id}", response_model=ProductOut)
@auth_required
async def get(request: Request, product_id: int):
    try:
        product: Product = get_product(product_id)
    except HTTPException as exception:
        raise exception
    except Exception:
        raise HTTPException(status_code=400, detail="Error getting product.")
    return ProductOut.from_orm(product)
