from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from app.routes.api_router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

