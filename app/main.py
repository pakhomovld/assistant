from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routes import register_routes
from app.config import settings

"""
Main application module for FastAPI.
Defines the app factory function and middleware setup.
"""

def create_app():
    """
    Application factory for creating and configuring the FastAPI app.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI()
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
    register_routes(app)
    return app

app = create_app()
