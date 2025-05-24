from pydantic import BaseModel, EmailStr, Field


class ClientCreate(BaseModel):
    first_name: str = Field(example="John")
    last_name: str = Field(example="Smith")
    email: EmailStr = Field(example="john.smith@gmail.com")
    cpf: str = Field(example="89659931050")
    address: str = Field(example="Rua das palmerinhas 205, Vale Verde - Monte Belo MG")
    phone: str = Field(example="(21) 98989-7878")


class ClientOut(BaseModel):
    id: int = Field(example=1)
    first_name: str = Field(example="John")
    last_name: str = Field(example="Smith")
    email: EmailStr = Field(example="john.smith@gmail.com")
    cpf: str = Field(example="89659931050")
    address: str = Field(example="Rua das palmerinhas 205, Vale Verde - Monte Belo MG")
    phone: str = Field(example="(21) 98989-7878")
