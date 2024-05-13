import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Assuming the token is 'test-token' which exists in the database
token = '0987654321'
headers = {"Authorization": f"Bearer {token}"}

def test_ping():
    response = client.get("/ping", headers=headers)
    assert response.status_code == 200
    assert response.json() == token

def test_read_items():
    response = client.get("/items/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_item():
    response = client.post("/items/?name=chips&price=6.50")
    assert response.status_code == 200
    assert response.json() == {"name": "chips", "price": 6.50}

def test_read_cart():
    response = client.get("/cart/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_cart():
    response = client.post("/cart/?item_id=1&quantity=1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "quantity": 1}


def test_delete_item():
    response = client.delete("/items/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}


def test_delete_cart():
    response = client.delete("/cart/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Cart item deleted successfully"}
