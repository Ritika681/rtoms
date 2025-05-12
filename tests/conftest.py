import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from database import engine, SessionLocal
from app.model.models import User, Order
import pytest_asyncio


@pytest_asyncio.fixture()
async def test_session():
    async with SessionLocal() as session:
        yield session
        await session.rollback()


'''
@pytest_asyncio.fixture(scope="session")
def event_loop():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
'''
@pytest_asyncio.fixture()
async def mock_user(test_session: AsyncSession):
    user = User(name="Test User", email="test@example.com")
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest_asyncio.fixture()
async def mock_order(test_session: AsyncSession, mock_user: User):
    order = Order(
        orderId=9999,
        status="Pending",
        items='["item1", "item2"]',
        tracking="TRACK9999",
        userId=mock_user.id
    )
    test_session.add(order)
    await test_session.commit()
    await test_session.refresh(order)
    return order
