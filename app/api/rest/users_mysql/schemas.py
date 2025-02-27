from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class PostBase(BaseModel):
    title: str
    content: str


class UserCreate(UserBase):
    pass


class UserPut(UserBase):
    pass


class UserPatch(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None


class UserInDB(UserBase):
    id: int
    posts: List[PostBase] = []


class PostCreate(PostBase):
    pass


class PostPut(PostBase):
    pass


class PostPatch(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None


class PostInDB(PostBase):
    id: int
    user_id: int
