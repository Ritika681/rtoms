import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app  # Import FastAPI app

# Use TestClient for synchronous calls (httpx doesn't require an actual HTTP server)
client = TestClient(app)

@pytest.mark.asyncio
async def test_get_all_orders():
    response = client.get("/api/orders/")
    assert response.status_code == 200
    orders = response.json()
    order_keys = {int(k) for k in orders.keys()}  # Convert keys to integers

    assert 1 in order_keys  # Ensure order with ID 1 exists

@pytest.mark.asyncio
async def test_get_single_order():
    response = client.get("/api/orders/1")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["orderId"] == 1
    assert json_data["status"] == "Processing"

@pytest.mark.asyncio
async def test_get_non_existing_order():
    response = client.get("/api/orders/999")  # Order does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"
