import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from fastapi import FastAPI
from app.routes import user, client, product, order
from app.core.config import settings

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[FastApiIntegration()],
    send_default_pii=True
)

app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(user.router, prefix="/auth", tags=["Users"])
app.include_router(client.router, prefix="/clients", tags=["Clients"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
