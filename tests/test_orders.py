import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_order():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/orders", json={
            "orderId": 2001,
            "status": "Processing",
            "items": ["book", "pen"],
            "tracking": "TRK2001",
            "userId": 1
        })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_order():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/orders/2001")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_orders():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/orders")
    assert response.status_code == 200
