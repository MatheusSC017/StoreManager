from sqlalchemy.exc import IntegrityError
from app.models.client import Client
from app.schemas.client_schema import ClientCreate, ClientOut
from app.controllers.client_controller import create_client, get_clients, get_client, update_client, delete_client
from fastapi import APIRouter, HTTPException, Request
from typing import List
from app.auth.decorators import auth_required

router = APIRouter()


@router.get("/", response_model=List[ClientOut])
@auth_required
async def get_all(request: Request):
    clients: List[Client] = get_clients()
    response = []
    for client in clients:
        response.append(ClientOut(
            id=client.id,
            first_name=client.first_name,
            last_name=client.last_name,
            email=client.email,
            cpf=client.cpf,
            address=client.address,
            phone=client.phone,
        ))
    return response


@router.post("/", response_model=ClientOut)
@auth_required
async def create(request: Request, client_data: ClientCreate):
    try:
        client: Client = create_client(client_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="E-mail already in use.")
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to register client.")
    return client


@router.put("/{client_id}", response_model=ClientOut)
@auth_required
async def update(request: Request, client_id: int, client_data: ClientCreate):
    try:
        client: Client = update_client(client_id, client_data)
        return ClientOut(
            id=client.id,
            first_name=client.first_name,
            last_name=client.last_name,
            email=client.email,
            cpf=client.cpf,
            address=client.address,
            phone=client.phone,
        )
    except HTTPException as exception:
        raise exception
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error updating client.")


@router.delete("/{client_id}", response_model=dict)
@auth_required
async def delete(request: Request, client_id: int):
    try:
        deleted: bool = delete_client(client_id)
        if deleted:
            return {"detail": "Client deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Error deleting client.")
    except HTTPException as exception:
        raise exception
    except Exception:
        raise HTTPException(status_code=400, detail="Error deleting client.")


@router.get("/{client_id}", response_model=ClientOut)
@auth_required
async def get(request: Request, client_id: int):
    try:
        client: Client = get_client(client_id)
    except HTTPException as exception:
        raise exception
    except Exception:
        raise HTTPException(status_code=400, detail="Error getting client.")
    return ClientOut(
        id=client.id,
        first_name=client.first_name,
        last_name=client.last_name,
        email=client.email,
        cpf=client.cpf,
        address=client.address,
        phone=client.phone,
    )
