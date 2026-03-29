from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth, services, users


def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(services.router)
    app.include_router(users.router)

    return app


app = create_app()
