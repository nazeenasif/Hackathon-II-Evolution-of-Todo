from fastapi import APIRouter
from src.api.v1.endpoints import tasks, auth


api_router = APIRouter()
api_router.include_router(tasks.router, prefix="", tags=["tasks"])
api_router.include_router(auth.router, prefix="", tags=["auth"])