from pydantic import BaseModel


class UserIn(BaseModel):
    name: str
    email: str
    age: int


class UserInPatch(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    age: int
