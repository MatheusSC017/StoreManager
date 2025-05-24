from app.db.session import Base, engine
from app.models.user import User
from app.models.client import Client
from app.models.product import Product
from app.models.order import Order

Base.metadata.create_all(bind=engine)
