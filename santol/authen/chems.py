from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from ..alchemy import BaseModel, DatesMixin


class User(BaseModel, DatesMixin):

    __tablename__ = 'user'

    username = Column(String(99), nullable=False, unique=True)
    password = Column(String(99), nullable=False)

    def __str__(self):
        return 'User(id={}, username={})'.format(self.id, self.username)


class Token(BaseModel, DatesMixin):

    __tablename__ = 'user_token'

    # The token used to grant access to the API.
    value = Column(String(100), unique=True)

    # The user that was granted the token.
    user_id = Column(Integer, ForeignKey('user.id'))

    # Create one-to-many relationship with the User model.
    user = relationship('User', backref='tokens')

    # The date and time the access token will expire.
    expired_at = Column(DateTime)

    def __str__(self):
        return "Token(id={}, user={}, value='{}', expired_at='{}')".format(
            self.id,
            self.user,
            self.value,
            self.expired_at
        )
