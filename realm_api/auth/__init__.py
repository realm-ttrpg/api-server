"""Authentication/authorization"""

# 3rd party
from fastapi import APIRouter, FastAPI

# local
from .routes import router


def setup_webapp(_app: FastAPI, app_router: APIRouter):
    app_router.include_router(router)
