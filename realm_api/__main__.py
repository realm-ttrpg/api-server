"""Entry point"""

# 3rd party
from uvicorn import run

# local
from os import environ

run(
    "realm_api.app:app",
    host=environ.get("REALM_HOST", "0.0.0.0"),
    port=int(environ.get("REALM_PORT", "5000")),
    lifespan="on",
)
