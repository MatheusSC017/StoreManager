from pydantic import BaseModel, Field
from enum import Enum


class AccessLevel(str, Enum):
    ADMIN = "Admin"
    REGULAR = "Regular"


class UserCreate(BaseModel):
    username: str = Field(example="john_smith")
    password: str = Field(example="password")
    access: AccessLevel = Field(example="Admin")


class UserOut(BaseModel):
    id: int = Field(example=1)
    username: str = Field(example="john_smith")
    access: AccessLevel = Field(example="Admin")

    class Config:
            orm_mode = True
