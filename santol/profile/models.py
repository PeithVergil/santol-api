from pydantic import BaseModel


class ProfileInput(BaseModel):
    fname: str
    lname: str


class ProfileInfo(BaseModel):
    id: int
    
    fname: str
    lname: str

    class Config:
        orm_mode = True
