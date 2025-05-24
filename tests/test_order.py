from types import SimpleNamespace
from unittest.mock import patch

fake_order_model = SimpleNamespace(**{
    "id": 1,
    "client_id": 1,
    "date": "2025-05-23",
    "status": "Pending",
    "order_products": [
        SimpleNamespace(**{
            "product_id": 5,
            "quantity": 3
        })
    ]
})

fake_order = {
    "id": 1,
    "client_id": 1,
    "date": "2025-05-23",
    "status": "Pending",
    "products": [
        {
            "product_id": 5,
            "quantity": 3
        }
    ]
}


@patch("app.routes.order.create_order", return_value=fake_order_model)
def test_create_order(mock_create, client):
    new_order = fake_order.copy()
    del new_order["id"]

    response = client.post("/orders", json=new_order)

    assert response.status_code == 201
    assert response.json() == fake_order


@patch("app.routes.order.update_order", return_value=fake_order_model)
def test_update_order(mock_create, client):
    order_data = fake_order.copy()
    order_id = order_data.pop("id")

    response = client.put(f"/orders/{order_id}", json=order_data)

    assert response.status_code == 202
    assert response.json() == fake_order


@patch("app.routes.order.delete_order", return_value={"detail": "Order deleted successfully"})
def test_delete_order(mock_create, client):
    response = client.delete(f"/orders/{fake_order.get('id')}")
    assert response.status_code == 202
    assert response.json() == {"detail": "Order deleted successfully"}


@patch("app.routes.order.get_order", return_value=fake_order_model)
def test_get_order(mock_create, client):
    response = client.get(f"/orders/{fake_order.get('id')}")
    assert response.status_code == 200
    assert response.json() == fake_order


@patch("app.routes.order.get_orders", return_value=[fake_order_model, fake_order_model])
def test_get_orders(mock_create, client):
    response = client.get(f"/orders")
    assert response.status_code == 200
    assert response.json() == [fake_order, fake_order]

