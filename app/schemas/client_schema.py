from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    cpf: str
    address: str
    phone: str


class ClientOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    cpf: str
    address: str
    phone: str
