from fastapi import FastAPI
from app.routes import user, client, product, order

app = FastAPI(title="FastAPI REST API Base")

app.include_router(user.router, prefix="/auth", tags=["Users"])
app.include_router(client.router, prefix="/clients", tags=["Clients"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
