from pydantic import BaseModel


class PinOut(BaseModel):
    id: int
    user_id: int
    title: str | None = None
    description: str | None = None
    href: str | None = None
    image: str | None = None
    rgb: str | None = None
    height: str | None = None


class PinIn(BaseModel):
    title: str | None = None
    description: str | None = None
    href: str | None = None
    height: str | None = None