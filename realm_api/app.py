"""FastAPI application"""

# stdlib
from contextlib import asynccontextmanager

# 3rd party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# local
from .api import router
from .db import init_db
from .rpc import init_pubsub, shutdown_pubsub


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function: startup -> yield -> shutdown"""

    await init_db()
    task = await init_pubsub()
    yield
    await shutdown_pubsub(task)


app = FastAPI(lifespan=lifespan)
"""Web application"""

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"],
)
app.include_router(router)
