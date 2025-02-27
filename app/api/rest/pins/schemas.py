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


class FilterParams(BaseModel):
    offset: int = 0
    limit: int = 10


class FilterWithValue(FilterParams):
    value: str
