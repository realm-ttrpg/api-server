# 3rd party
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlmodel import select, Session

# local
from ..db import get_session
from ..models.user_session import UserSession


def require_login(
    user_id: str = Depends(APIKeyHeader(name="X-Realm-User")),
    realm_token: str = Depends(APIKeyHeader(name="X-Realm-Token")),
    session: Session = Depends(get_session),
):
    user_session = session.exec(
        select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.realm_token == realm_token,
        )
    ).one_or_none()

    if not user_session:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user_session
