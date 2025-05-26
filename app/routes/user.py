from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserOut
from app.controllers.user_controller import create_user, get_user
from app.auth.jwt_handler import create_token, verify_token
from app.core.security import check_password
from app.auth.authentication import admin_required
from app.schemas.auth_schema import TokenResponse, TokenType, RefreshRequest

router = APIRouter()


@router.post("/register", dependencies=[Depends(admin_required)], response_model=UserOut, description="New user registration (Only admin access).")
async def create(request: Request, user_data: UserCreate):
    try:
        user: User = create_user(user_data)
        return UserOut(
            id=user.id,
            username=user.username,
            access=user.access
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already in use.")


@router.post("/login", response_model=TokenResponse, description="User authentication.")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = get_user(form_data.username)
    if user and not check_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_data = {"user": str(user.id), "username": user.username, "access": user.access}
    access_token = create_token(user_data, TokenType.ACCESS)
    refresh_token = create_token(user_data, TokenType.REFRESH)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse, description="JWT token refresh.")
def refresh(request: RefreshRequest):
    payload = verify_token(request.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_data = {"user": payload["user"], "username": payload["username"], "access": payload["access"]}
    return TokenResponse(
        access_token=create_token(user_data, TokenType.ACCESS),
        refresh_token=create_token(user_data, TokenType.REFRESH)
    )
