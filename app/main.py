from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routes import register_routes
from app.config import settings

def create_app():
    app = FastAPI()
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
    register_routes(app)
    return app

app = create_app()

