from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return crypt_context.hash(password)


def check_password(password: str, hashed_password: str) -> bool:
    return crypt_context.verify(password, hashed_password)
