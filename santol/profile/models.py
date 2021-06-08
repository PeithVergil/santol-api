from pydantic import BaseModel


class ProfileInfo(BaseModel):
    id: int
    
    fname: str
    lname: str

    class Config:
        orm_mode = True
