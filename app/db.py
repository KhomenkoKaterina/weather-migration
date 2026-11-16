from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import get_database_url


def get_session_factory(url: str | None = None):
    engine = create_engine(url or get_database_url(), pool_pre_ping=True)
    return sessionmaker(bind=engine, expire_on_commit=False)