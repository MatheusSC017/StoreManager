from app.schemas.user_schema import AccessLevel
from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import verify_token

bearer_scheme = HTTPBearer()


async def auth_required(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


async def admin_required(payload: dict = Depends(auth_required)):
    if payload.get("access") != AccessLevel.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload
