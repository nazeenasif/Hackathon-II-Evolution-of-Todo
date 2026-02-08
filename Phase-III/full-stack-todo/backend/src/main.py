from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

from src.api.v1.router import api_router
from src.core.config import settings
from src.core.logging import setup_logging
from src.core.database import create_db_and_tables
from src.models.user import User
from src.models.task import Task


def create_app() -> FastAPI:
    # Setup logging
    setup_logging()

    app = FastAPI(
        title="Todo Backend API",
        description="Backend Core & Database Layer for Multi-User Todo Application",
        version="0.1.0",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://hackathon-ii-evolution-of-todo-jade.vercel.app",
            "http://localhost:3000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handler for all unhandled errors
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        print("Exception occurred:", str(exc))
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "message": str(exc),
                "trace": traceback.format_exc()
            }
        )

    # Create database tables at startup
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    # Include API routes
    app.include_router(api_router, prefix="/api")

    # Root endpoint
    @app.get("/")
    def read_root():
        return {"message": "Welcome to Todo Backend API"}

    return app


app = create_app()


def main():
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )


if __name__ == "__main__":
    main()