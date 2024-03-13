# 3rd party
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_webapp(app: FastAPI, _router: APIRouter):
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_headers=["*"],
        allow_methods=["*"],
        allow_origins=["*"],
    )
