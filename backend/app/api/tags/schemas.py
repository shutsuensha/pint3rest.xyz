from pydantic import BaseModel


class TagsIn(BaseModel):
    pin_id: int
    tags: list[str]