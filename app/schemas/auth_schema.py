from pydantic import BaseModel
from enum import Enum


class TokenType(str, Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
