# stdlib
import os

# 3rd party
from sqlmodel import create_engine, Session, SQLModel

engine = create_engine(
    os.environ.get("DB_URL", "postgresql://realm:realm@localhost/realm")
)


def get_session():
    with Session(engine) as session:
        yield session


def setup_webapp(*_):
    from .models.user_session import UserSession  # noqa: F401

    SQLModel.metadata.create_all(engine)
