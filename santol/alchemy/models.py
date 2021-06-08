from sqlalchemy import (
    Column,
    Integer,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base


class Base:
    id = Column(Integer, primary_key=True)


# Create the base model class.
BaseModel = declarative_base(cls=Base)


class DatesMixin:
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
