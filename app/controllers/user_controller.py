from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.db.session import SessionLocal
from app.core.security import hash_password


def create_user(user_data: UserCreate) -> User:
    db = SessionLocal()
    hashed_password = hash_password(user_data.password)
    user = User(username=user_data.username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def get_user(username: str) -> User:
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user
