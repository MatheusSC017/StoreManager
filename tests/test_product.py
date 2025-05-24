from unittest.mock import patch

fake_product = {
        "id": 1,
        "description": "Chocolate Bar",
        "value": 12.5,
        "barcode": "567671948894",
        "section": "Section B",
        "stock": 250,
        "expiration_date": "2025-07-24"
    }


@patch("app.routes.product.create_product", return_value=fake_product)
def test_create_product(mock_create, client):
    new_product = fake_product.copy()
    del new_product["id"]

    response = client.post("/products", json=new_product)

    assert response.status_code == 201
    assert response.json() == fake_product


@patch("app.routes.product.update_product", return_value=fake_product)
def test_update_product(mock_create, client):
    product_data = fake_product.copy()
    product_id = product_data.pop("id")

    response = client.put(f"/products/{product_id}", json=product_data)

    assert response.status_code == 202
    assert response.json() == fake_product


@patch("app.routes.product.delete_product", return_value={"detail": "Product deleted successfully"})
def test_delete_product(mock_create, client):
    response = client.delete(f"/products/{fake_product.get('id')}")
    assert response.status_code == 202
    assert response.json() == {"detail": "Product deleted successfully"}


@patch("app.routes.product.get_product", return_value=fake_product)
def test_get_product(mock_create, client):
    response = client.get(f"/products/{fake_product.get('id')}")
    assert response.status_code == 200
    assert response.json() == fake_product


@patch("app.routes.product.get_products", return_value=[fake_product, fake_product])
def test_get_products(mock_create, client):
    response = client.get(f"/products")
    assert response.status_code == 200
    assert response.json() == [fake_product, fake_product]
