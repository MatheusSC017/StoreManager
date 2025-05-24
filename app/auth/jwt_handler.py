from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.schemas.auth_schema import TokenType
from app.core.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_token(data: dict, type: TokenType):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES if type == TokenType.ACCESS else REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "expire": expire.isoformat(),
        "type": TokenType.ACCESS if type == TokenType.ACCESS else TokenType.REFRESH
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

        expire_str = payload.get("expire")
        if not expire_str:
            return None

        expire_time = datetime.fromisoformat(expire_str)
        if expire_time < datetime.now():
            return None

        return payload
    except JWTError:
        return None
