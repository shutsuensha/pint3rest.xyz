from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    age: int

class UserInResponse(BaseModel):
    id: str
    name: str
    email: str
    age: int