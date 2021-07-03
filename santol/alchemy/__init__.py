from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import BaseModel, DatesMixin
from ..settings import DATABASE


SessionMaker = sessionmaker(bind=create_engine(DATABASE))


def alchemy_session():
    session = SessionMaker()
    try:
        yield session
    finally:
        session.close()


__all__ = [
    'Session',
    'BaseModel',
    'DatesMixin',
    'SessionMaker',
    'alchemy_session',
]
