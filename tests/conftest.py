import pytest
import asyncio
import sys
import pytest_asyncio

@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Ensure a fresh event loop is used for Windows compatibility."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
