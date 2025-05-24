from pydantic import BaseModel, Field, ConfigDict
from datetime import date as dt_date
from typing import Optional


class ProductCreate(BaseModel):
    description: str = Field(json_schema_extra={"example": "Chocolate Bar"})
    value: float = Field(json_schema_extra={"example": 12.5})
    barcode: str = Field(json_schema_extra={"example": "567671948894"})
    section: str = Field(json_schema_extra={"example": "Section B"})
    stock: int = Field(json_schema_extra={"example": 250})
    expiration_date: Optional[dt_date] = Field(json_schema_extra={"example": "2025-07-24"})


class ProductOut(BaseModel):
    id: int = Field(json_schema_extra={"example": 1})
    description: str = Field(json_schema_extra={"example": "Chocolate Bar"})
    value: float = Field(json_schema_extra={"example": 12.5})
    barcode: str = Field(json_schema_extra={"example": "567671948894"})
    section: str = Field(json_schema_extra={"example": "Section B"})
    stock: int = Field(json_schema_extra={"example": 250})
    expiration_date: Optional[dt_date] = Field(json_schema_extra={"example": "2025-07-24"})

    model_config = ConfigDict(from_attributes=True)
