import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app
from database import orders_collection  # Import MongoDB collection

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
async def clear_test_db():
    """Ensure the test database is cleared before each test"""
    await orders_collection.delete_many({})  # Make sure this is awaited

@pytest.mark.asyncio
async def test_create_order():
    response = await asyncio.to_thread(client.post, "/api/orders", json={
        "orderId": 1001,
        "status": "Processing",
        "items": ["itemA", "itemB"],
        "tracking": "In warehouse"
    })
    assert response.status_code == 200, response.text
    assert response.json()["message"] == "Order created successfully"

@pytest.mark.asyncio
async def test_get_order():
    await test_create_order()  # Ensure an order exists first
    response = await asyncio.to_thread(client.get, "/api/orders/1001")
    assert response.status_code == 200
    assert response.json()["orderId"] == 1001

@pytest.mark.asyncio
async def test_get_order_status():
    await test_create_order()
    response = await asyncio.to_thread(client.get, "/api/orders/1001/status")
    assert response.status_code == 200
    assert "status" in response.json()

@pytest.mark.asyncio
async def test_update_order_status():
    await test_create_order()
    response = await asyncio.to_thread(client.put, "/api/orders/1001/status", json={"status": "Shipped"})
    assert response.status_code == 200
    assert response.json()["message"] == "Order status updated successfully"

@pytest.mark.asyncio
async def test_delete_order():
    await test_create_order()
    response = await asyncio.to_thread(client.delete, "/api/orders/1001")
    assert response.status_code == 200
    assert response.json()["message"] == "Order deleted successfully"
