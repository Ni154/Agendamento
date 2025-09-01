from pydantic import BaseModel

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    role: str
    class Config:
        from_attributes = True

