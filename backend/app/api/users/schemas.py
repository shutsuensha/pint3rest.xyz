from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None


class UserOut(BaseModel):
    id: int
    username: str
    image: str | None = None
    email: EmailStr | None = None
    verified: bool | None = None


class PasswordResetRequestModel(BaseModel):
    username: str
    email: EmailStr
    password: str