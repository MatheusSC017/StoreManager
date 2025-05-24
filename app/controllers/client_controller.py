from fastapi import HTTPException

from app.models.client import Client
from app.schemas.client_schema import ClientCreate
from app.db.session import SessionLocal
from typing import List


def create_client(client_data: ClientCreate) -> Client:
    db = SessionLocal()
    client = Client(first_name=client_data.first_name, last_name=client_data.last_name, email=client_data.email,
                    cpf=client_data.cpf, address=client_data.address, phone=client_data.phone)
    db.add(client)
    db.commit()
    db.refresh(client)
    db.close()
    return client


def update_client(client_id: int, client_data: ClientCreate) -> Client:
    db = SessionLocal()
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        db.close()
        raise HTTPException(status_code=404, detail="Client not found")
    client.first_name = client_data.first_name
    client.last_name = client_data.last_name
    client.email = client_data.email
    client.cpf = client_data.cpf
    client.address = client_data.address
    client.phone = client_data.phone

    db.commit()
    db.refresh(client)
    db.close()
    return client


def delete_client(id: int) -> bool:
    db = SessionLocal()
    client = db.query(Client).filter(Client.id == id).first()

    if not client:
        db.close()
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
    db.close()
    return True


def get_clients() -> List[Client]:
    db = SessionLocal()
    client = db.query(Client).all()
    db.close()
    return client


def get_client(client_id: int) -> Client:
    db = SessionLocal()
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        db.close()
        raise HTTPException(status_code=404, detail="Client not found")
    return client
