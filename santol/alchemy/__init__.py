from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import BaseModel, DatesMixin
from ..settings import DATABASE


SessionMaker = sessionmaker(bind=create_engine(DATABASE))


@contextmanager
def AlchemySession(commit=True):
    session = SessionMaker()
    try:
        yield session
        if commit:
            session.commit()
    finally:
        session.close()


__all__ = [
    'Session',
    'BaseModel',
    'DatesMixin',
    'AlchemySession',
]
