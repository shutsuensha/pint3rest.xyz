from sqlalchemy import Table, Column, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from datetime import date



class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    image: Mapped[str | None] = mapped_column(String(200), default=None)
    
    email: Mapped[str | None] = mapped_column(String(200), default=None)
    verified: Mapped[bool | None] = mapped_column(Boolean, default=False)