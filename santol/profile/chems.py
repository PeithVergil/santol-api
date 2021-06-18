from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from ..alchemy import BaseModel, DatesMixin


class Profile(BaseModel, DatesMixin):

    __tablename__ = 'user_profile'

    # The user that was granted the token.
    # NOTE: A user should only have one profile.
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)

    # Create one-to-many relationship with the User model.
    user = relationship('User', backref='profile', uselist=False)

    fname = Column(String(100))
    lname = Column(String(100))

    def __str__(self):
        return "Profile(id={}, user={}, fname='{}', lname='{}')".format(
            self.id,
            self.user,
            self.fname,
            self.lname,
        )
