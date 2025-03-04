import pytest
import asyncio
import sys

@pytest.fixture(scope="session")
def event_loop():
    """Ensures an event loop works correctly on Windows."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
