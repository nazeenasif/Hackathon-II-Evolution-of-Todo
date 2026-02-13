from fastapi import APIRouter
from src.api.v1.endpoints import tasks, auth
from src.api.v1.endpoints.chat import router as chat_router
from src.api.v1.endpoints.conversations import router as conversations_router


api_router = APIRouter()
api_router.include_router(tasks.router, prefix="", tags=["tasks"])
api_router.include_router(auth.router, prefix="", tags=["auth"])
api_router.include_router(chat_router, prefix="", tags=["chat"])
api_router.include_router(conversations_router, prefix="", tags=["conversations"])