from pydantic import BaseModel


class LikeOut(BaseModel):
    id: int
    user_id: int
    pin_id: int | None = None
    comment_id: int | None = None
