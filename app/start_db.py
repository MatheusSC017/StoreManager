from app.db.session import Base, engine, SessionLocal
from app.models.user import User
from app.models.client import Client
from app.models.product import Product
from app.models.order import Order
from app.schemas.user_schema import AccessLevel
from app.core.security import hash_password


def init_db():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        existing_user = db.query(User).filter_by(username="admin").first()
        if not existing_user:
            admin = User(
                username="admin",
                hashed_password=hash_password("admin"),
                access=AccessLevel.ADMIN
            )
            db.add(admin)
            db.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

