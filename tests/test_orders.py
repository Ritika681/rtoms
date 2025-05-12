import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from database import get_session
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_get_all_orders():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/orders")
    assert response.status_code == 200

'''
@pytest.mark.asyncio
async def test_get_order(mock_order, test_session):
    app.dependency_overrides[get_session] = lambda: test_session
    mock_order = await mock_order 

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/api/orders/{mock_order.orderId}")
        print(response.text)
        assert response.status_code == 200
        assert response.json()["orderId"] == mock_order.orderId

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_order(mock_user):
    #mock_user = await mock_user
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/orders", json={
            "orderId": 2002,
            "status": "Shipped",
            "items": ["itemX"],
            "tracking": "TRK2002",
            "userId": mock_user.id
        })
        assert response.status_code == 200
'''