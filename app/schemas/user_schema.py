from pydantic import BaseModel, Field
from enum import Enum


class AccessLevel(str, Enum):
    ADMIN = "Admin"
    REGULAR = "Regular"


class UserCreate(BaseModel):
    username: str = Field(json_schema_extra={"example": "john_smith"})
    password: str = Field(json_schema_extra={"example": "password"})
    access: AccessLevel = Field(json_schema_extra={"example": "Admin"})


class UserOut(BaseModel):
    id: int = Field(json_schema_extra={"example": 1})
    username: str = Field(json_schema_extra={"example": "john_smith"})
    access: AccessLevel = Field(json_schema_extra={"example": "Admin"})
