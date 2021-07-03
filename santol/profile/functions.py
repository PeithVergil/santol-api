import logging

from fastapi import HTTPException, security, status
from datetime import datetime
from sqlalchemy import exc

from .chems import Profile
from .models import ProfileInfo
from ..errors import DatabaseError
from ..alchemy import Session


logger = logging.getLogger(__name__)


bearer = security.HTTPBearer()


def select_profile(user_id: int, db: Session) -> ProfileInfo:
    query = (
        db
        .query(Profile)
        .filter(Profile.user_id == user_id)
    )
    profile = query.first()

    if profile is None:
        logger.info('Profile not found.')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Profile does not exist')
    
    return ProfileInfo.from_orm(profile)


def create_profile(user_id: int, fname: str, lname: str, db: Session) -> ProfileInfo:
    created_at = datetime.utcnow()

    profile = Profile(
        fname=fname,
        lname=lname,
        user_id=user_id,
        created_at=created_at,
    )

    db.add(profile)

    try:
        db.commit()
    except exc.IntegrityError as error:
        db.rollback()

        logger.exception('Failed to create a new profile.')

        errnum, errmsg = error.orig.args
        title = 'Failed to create a new profile.'
        info = {
            'code': errnum,
            'text': errmsg,
        }
        raise DatabaseError(info, title)
    
    return ProfileInfo.from_orm(profile)


def delete_profile(profile_id: int, db: Session) -> bool:
    query = (
        db
        .query(Profile)
        .filter(Profile.id == profile_id)
    )

    query.delete()
    
    try:
        db.commit()
    except exc.IntegrityError as error:
        db.rollback()

        logger.exception('Failed to delete the profile.')

        return False

    return True
