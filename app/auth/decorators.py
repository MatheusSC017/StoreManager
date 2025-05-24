from fastapi import Request, HTTPException
from functools import wraps
from app.auth.jwt_handler import verify_token


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing token")

        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await func(*args, **kwargs)
    return wrapper
