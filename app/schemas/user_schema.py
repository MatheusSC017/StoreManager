from pydantic import BaseModel
from enum import Enum


class AccessLevel(str, Enum):
    ADMIN = "Admin"
    REGULAR = "Regular"


class UserCreate(BaseModel):
    username: str
    password: str
    access: AccessLevel


class UserOut(BaseModel):
    id: int
    username: str
    access: AccessLevel

    class Config:
        orm_mode = True
