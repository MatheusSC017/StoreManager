from unittest.mock import patch
from types import SimpleNamespace

fake_client = {
        "id": 1,
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@gmail.com",
        "cpf": "89659931050",
        "address": "Rua das palmerinhas 205, Vale Verde - Monte Belo MG",
        "phone": "(21) 98989-7878"
    }


@patch("app.routes.client.create_client", return_value=fake_client)
def test_create_client(mock_create, client):
    new_client = fake_client.copy()
    del new_client["id"]

    response = client.post("/clients", json=new_client)

    assert response.status_code == 201
    assert response.json() == fake_client


@patch("app.routes.client.update_client", return_value=SimpleNamespace(**fake_client))
def test_update_client(mock_create, client):
    client_data = fake_client.copy()
    client_id = client_data.pop("id")

    response = client.put(f"/clients/{client_id}", json=client_data)

    assert response.status_code == 202
    assert response.json() == fake_client


@patch("app.routes.client.delete_client", return_value={"detail": "Client deleted successfully"})
def test_delete_client(mock_create, client):
    response = client.delete(f"/clients/{fake_client.get('id')}")
    assert response.status_code == 202
    assert response.json() == {"detail": "Client deleted successfully"}


@patch("app.routes.client.get_client", return_value=SimpleNamespace(**fake_client))
def test_get_client(mock_create, client):
    response = client.get(f"/clients/{fake_client.get('id')}")
    assert response.status_code == 200
    assert response.json() == fake_client


@patch("app.routes.client.get_clients", return_value=[SimpleNamespace(**fake_client), SimpleNamespace(**fake_client)])
def test_get_clients(mock_create, client):
    response = client.get(f"/clients")
    assert response.status_code == 200
    assert response.json() == [fake_client, fake_client]
