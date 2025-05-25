import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import user, client, product, order
from app.core.config import settings

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[FastApiIntegration()],
    send_default_pii=True
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="This is a RESTful API designed to manage a company's stock and sales operations. It includes core "
                "tables for Clients, Products, and Orders, allowing efficient tracking of inventory, customer data, "
                "and transaction history.")


app.mount("/images", StaticFiles(directory="static/images"), name="images")

app.include_router(user.router, prefix="/auth", tags=["Users"])
app.include_router(client.router, prefix="/clients", tags=["Clients"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
