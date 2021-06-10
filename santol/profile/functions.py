import logging

from fastapi import HTTPException, Depends, security, status
from datetime import datetime
from sqlalchemy import exc

from .chems import Profile
from .models import ProfileInfo
from ..errors import DatabaseError
from ..alchemy import AlchemySession


logger = logging.getLogger(__name__)


bearer = security.HTTPBearer()


def select_profile(user_id: int, session=None) -> ProfileInfo:
    if session is not None:
        return ackchyually_select_profile(user_id, session)
    
    with AlchemySession(False) as session:
        return ackchyually_select_profile(user_id, session)


def ackchyually_select_profile(user_id: int, session: AlchemySession) -> ProfileInfo:
    query = (
        session
        .query(Profile)
        .filter(Profile.user_id == user_id)
    )
    profile = query.first()

    if profile is None:
        logger.info('Profile not found.')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Profile does not exist')
    
    return ProfileInfo.from_orm(profile)


def create_profile(user_id: int, fname: str, lname: str, session=None) -> ProfileInfo:
    if session is not None:
        return ackchyually_create_profile(user_id, fname, lname, session)
    
    with AlchemySession(False) as session:
        return ackchyually_create_profile(user_id, fname, lname, session)
    

def ackchyually_create_profile(user_id: int, fname: str, lname: str, session: AlchemySession) -> ProfileInfo:
    created_at = datetime.utcnow()

    profile = Profile(
        fname=fname,
        lname=lname,
        user_id=user_id,
        created_at=created_at,
    )

    session.add(profile)

    try:
        session.commit()
    except exc.IntegrityError as error:
        session.rollback()

        logger.exception('Failed to create a new profile.')

        errnum, errmsg = error.orig.args
        title = 'Failed to create a new profile.'
        info = {
            'code': errnum,
            'text': errmsg,
        }
        raise DatabaseError(info, title)
    
    return ProfileInfo.from_orm(profile)


def delete_profile(profile_id: int, session=None) -> bool:
    if session is not None:
        return ackchyually_delete_profile(profile_id, session)
    
    with AlchemySession(False) as session:
        return ackchyually_delete_profile(profile_id, session)


def ackchyually_delete_profile(profile_id: str, session: AlchemySession) -> bool:
    query = (
        session
        .query(Profile)
        .filter(Profile.id == profile_id)
    )

    query.delete()
    
    try:
        session.commit()
    except exc.IntegrityError as error:
        session.rollback()

        logger.exception('Failed to delete the profile.')

        return False

    return True
