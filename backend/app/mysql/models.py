from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    content: Mapped[str] = mapped_column(String(500))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    # Связь с пользователем (Many-to-One)
    owner: Mapped["User"] = relationship("User", back_populates="posts")