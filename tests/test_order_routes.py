import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from main import app
from database import orders_collection  # Import MongoDB collection

client = TestClient(app)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def clear_test_db():
    """Ensure the test database is cleared before each test"""
    await orders_collection.delete_many({})  # Properly await MongoDB cleanup

def test_create_order(clear_test_db):  # No `async`
    response = client.post("/api/orders", json={
        "orderId": 1001,
        "status": "Processing",
        "items": ["itemA", "itemB"],
        "tracking": "In warehouse"
    })
    assert response.status_code == 200, response.text
    assert response.json()["message"] == "Order created successfully"

def test_get_order(clear_test_db):  # No `async`
    test_create_order(clear_test_db)  # Ensure an order exists first
    response = client.get("/api/orders/1001")
    assert response.status_code == 200
    assert response.json()["orderId"] == 1001

def test_get_order_status(clear_test_db):  # No `async`
    test_create_order(clear_test_db)
    response = client.get("/api/orders/1001/status")
    assert response.status_code == 200
    assert "status" in response.json()

def test_update_order_status(clear_test_db):  # No `async`
    test_create_order(clear_test_db)
    response = client.put("/api/orders/1001/status", json={"status": "Shipped"})
    assert response.status_code == 200
    assert response.json()["message"] == "Order status updated successfully"

def test_delete_order(clear_test_db):  # No `async`
    test_create_order(clear_test_db)
    response = client.delete("/api/orders/1001")
    assert response.status_code == 200
    assert response.json()["message"] == "Order deleted successfully"
