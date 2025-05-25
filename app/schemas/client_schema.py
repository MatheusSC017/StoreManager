from pydantic import BaseModel, EmailStr, Field


class ClientCreate(BaseModel):
    first_name: str = Field(..., json_schema_extra={"example": "John"})
    last_name: str = Field(..., json_schema_extra={"example": "Smith"})
    email: EmailStr = Field(..., json_schema_extra={"example": "john.smith@gmail.com"})
    cpf: str = Field(..., json_schema_extra={"example": "89659931050"})
    address: str = Field(..., json_schema_extra={"example": "Rua das palmerinhas 205, Vale Verde - Monte Belo MG"})
    phone: str = Field(..., json_schema_extra={"example": "(21) 98989-7878"})


class ClientOut(BaseModel):
    id: int = Field(..., json_schema_extra={"example": 1})
    first_name: str = Field(..., json_schema_extra={"example": "John"})
    last_name: str = Field(..., json_schema_extra={"example": "Smith"})
    email: EmailStr = Field(..., json_schema_extra={"example": "john.smith@gmail.com"})
    cpf: str = Field(..., json_schema_extra={"example": "89659931050"})
    address: str = Field(..., json_schema_extra={"example": "Rua das palmerinhas 205, Vale Verde - Monte Belo MG"})
    phone: str = Field(..., json_schema_extra={"example": "(21) 98989-7878"})
