# from fastapi import FastAPI
# from contextlib import asynccontextmanager
# from database import init_db
# from routes.order_routes import router as order_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup actions
#     await init_db()
#     yield
#     # Shutdown actions (optional cleanup)

# app = FastAPI(lifespan=lifespan)

# app.include_router(order_router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0",port=8000)


from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routes.order_routes import router as order_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(order_router)
