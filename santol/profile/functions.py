import logging

from fastapi import HTTPException, Depends, security, status
from sqlalchemy import desc

from .chems import Profile
from .models import ProfileInfo
from ..authen import Token
from ..alchemy import AlchemySession


logger = logging.getLogger(__name__)


bearer = security.HTTPBearer()


def select_profile(authorization: security.HTTPAuthorizationCredentials = Depends(bearer)) -> ProfileInfo:
    with AlchemySession(False) as session:
        query = (
            session
            .query(Token)
            .filter(Token.value == authorization.credentials)
            .order_by(desc(Token.created_at))
        )
        token = query.first()

        if token is None:
            logger.info('Token not found.')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Token does not exist',
            )
        
        query = (
            session
            .query(Profile)
            .filter(Profile.user_id == token.user_id)
        )
        profile = query.first()

        if profile is None:
            logger.info('Profile not found.')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Profile does not exist',
            )
        
        return ProfileInfo.from_orm(profile)
