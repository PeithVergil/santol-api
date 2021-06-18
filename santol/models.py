from typing import Optional
from pydantic import BaseModel


class Profile(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
