# 3rd party
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

# local
from ..db import get_session
from ..models.user_session import UserSession


async def require_login(
    user_id: str = Depends(APIKeyHeader(name="X-Realm-User")),
    realm_token: str = Depends(APIKeyHeader(name="X-Realm-Token")),
    session: AsyncSession = Depends(get_session),
):
    user_session = (
        await session.execute(
            select(UserSession).where(
                UserSession.user_id == user_id,
                UserSession.realm_token == realm_token,
            )
        )
    ).scalar_one_or_none()

    if not user_session:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user_session
