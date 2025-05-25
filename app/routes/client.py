from sqlalchemy.exc import IntegrityError
from app.models.client import Client
from app.schemas.client_schema import ClientCreate, ClientOut
from app.auth.authentication import auth_required
from app.controllers.client_controller import create_client, get_clients, get_client, update_client, delete_client
from fastapi import Depends, APIRouter, HTTPException, Request
from typing import List

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(auth_required)],
    response_model=List[ClientOut],
    description="Retrieve a list of all clients.")
async def get_all(request: Request):
    clients: List[Client] = get_clients()
    response: List[ClientOut] = []
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


@router.post(
    "/",
    dependencies=[Depends(auth_required)],
    response_model=ClientOut,
    status_code=201,
    description="Create a new client.")
async def create(request: Request, client_data: ClientCreate):
    try:
        client: Client = create_client(client_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="E-mail/CPF already in use.")
    return client


@router.put(
    "/{client_id}",
    dependencies=[Depends(auth_required)],
    response_model=ClientOut,
    status_code=202,
    description="Update a client's information.")
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
    except IntegrityError:
        raise HTTPException(status_code=400, detail="E-mail/CPF already in use.")
    except HTTPException as exception:
        raise exception


@router.delete(
    "/{client_id}",
    dependencies=[Depends(auth_required)],
    response_model=dict,
    status_code=202,
    description="Delete a client.")
async def delete(request: Request, client_id: int):
    try:
        deleted: bool = delete_client(client_id)
        if deleted:
            return {"detail": "Client deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Error deleting client.")
    except HTTPException as exception:
        raise exception


@router.get(
    "/{client_id}",
    dependencies=[Depends(auth_required)],
    response_model=ClientOut,
    description="Get details of a specific client.")
async def get(request: Request, client_id: int):
    try:
        client: Client = get_client(client_id)
    except HTTPException as exception:
        raise exception
    return ClientOut(
        id=client.id,
        first_name=client.first_name,
        last_name=client.last_name,
        email=client.email,
        cpf=client.cpf,
        address=client.address,
        phone=client.phone,
    )
