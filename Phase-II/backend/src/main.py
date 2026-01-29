from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

    # Add CORS middleware to allow requests from Next.js frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "https://full-stack-todo-gamma.vercel.app/"
            ],  # Allow requests from Next.js frontend
        allow_credentials=True,  # Allow cookies and credentials
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

    # Create all database tables at startup
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    # Include API router
    app.include_router(api_router, prefix="/api")

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