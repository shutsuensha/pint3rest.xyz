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
    banner_image: str | None = None
    description: str | None = None
    instagram: str | None = None
    tiktok: str | None = None
    telegram: str | None = None
    pinterest: str | None = None


class UserPatch(BaseModel):
    username: str | None = None
    description: str | None = None
    instagram: str | None = None
    tiktok: str | None = None
    telegram: str | None = None
    pinterest: str | None = None


class PasswordResetRequestModel(BaseModel):
    username: str
    email: EmailStr
    password: str
