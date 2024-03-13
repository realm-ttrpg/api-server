# 3rd party
from fastapi import APIRouter, FastAPI, HTTPException, status
from aiohttp import ClientSession

# local
from .models.login import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(login_request: LoginRequest) -> LoginResponse:
    async with ClientSession() as session:
        session.headers.add("Authorization", f"Bearer {login_request.token}")

        async with session.get(
            "https://discord.com/api/v10/oauth2/@me"
        ) as response:
            obj = await response.json()

            if obj["user"]["id"] != login_request.user_id:
                raise HTTPException(status.HTTP_403_FORBIDDEN)

    # TODO generate, store, and return session token
    return LoginResponse(token="ok")


@router.post("/logout")
def logout():
    # TODO remove session token from DB
    pass


def setup_webapp(app: FastAPI, _router: APIRouter):
    app.include_router(router)
