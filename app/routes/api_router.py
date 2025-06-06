from fastapi import APIRouter
from app.routes.order_routes import router as order_router
from app.routes.user_routes import router as user_router

api_router = APIRouter()
api_router.include_router(order_router)
api_router.include_router(user_router)
