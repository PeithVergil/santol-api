from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    
    username: str

    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserToken(BaseModel):
    value: str

    created_at: datetime
    expired_at: datetime

    class Config:
        orm_mode = True


class UserCredentials(BaseModel):
    username: str
    password: str
