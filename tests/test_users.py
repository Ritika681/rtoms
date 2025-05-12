import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_user_orders():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/users/1/orders")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_order_history():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/users/1/order-history")
    assert response.status_code == 200
