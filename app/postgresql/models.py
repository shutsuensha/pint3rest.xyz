from datetime import datetime, timezone

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    google_id: Mapped[str | None] = mapped_column(String(200), default=None)

    username: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str | None] = mapped_column(String(200), default=None)
    image: Mapped[str | None] = mapped_column(String(200), default=None)
    banner_image: Mapped[str | None] = mapped_column(String(200), default=None)

    description: Mapped[str | None] = mapped_column(String(400), default=None)

    instagram: Mapped[str | None] = mapped_column(String(200), default=None)
    tiktok: Mapped[str | None] = mapped_column(String(200), default=None)
    telegram: Mapped[str | None] = mapped_column(String(200), default=None)
    pinterest: Mapped[str | None] = mapped_column(String(200), default=None)

    email: Mapped[str | None] = mapped_column(String(200), default=None)
    verified: Mapped[bool | None] = mapped_column(Boolean, default=False)

    chat_color: Mapped[str | None] = mapped_column(String(100), default="blue")
    chat_size: Mapped[int | None] = mapped_column(Integer, default=384)
    side_open: Mapped[bool | None] = mapped_column(Boolean, default=True)

    selected_board: Mapped[int | None] = mapped_column(
        ForeignKey("boards.id", ondelete="SET NULL", name="fk_users_selected_board"), default=None
    )

    recommendation_created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), default=None
    )


class PinsOrm(Base):
    __tablename__ = "pins"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str | None] = mapped_column(String(200), default=None)
    description: Mapped[str | None] = mapped_column(String(400), default=None)
    href: Mapped[str | None] = mapped_column(String(200), default=None)

    image: Mapped[str | None] = mapped_column(String(200), default=None)
    videoPreview: Mapped[str | None] = mapped_column(String(200), default=None)

    rgb: Mapped[str | None] = mapped_column(String(100), default=None)

    height: Mapped[str | None] = mapped_column(String(100), default=None)


class BoardsOrm(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", name="fk_boards_user_id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class TagsOrm(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class CommentsOrm(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)

    pin_id: Mapped[int | None] = mapped_column(
        ForeignKey("pins.id", ondelete="CASCADE"), default=None
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), default=None
    )

    content: Mapped[str | None] = mapped_column(String(400), default=None)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    image: Mapped[str | None] = mapped_column(String(200), default=None)


class LikesOrm(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)

    pin_id: Mapped[int | None] = mapped_column(
        ForeignKey("pins.id", ondelete="CASCADE"), default=None
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), default=None
    )


class SubsrciptionsOrm(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)

    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)


class ChatOrm(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_1_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user_2_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)


class MessageOrm(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    user_id_: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str | None] = mapped_column(String(400), default=None)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    image: Mapped[str | None] = mapped_column(String(200), default=None)

    is_read: Mapped[bool | None] = mapped_column(Boolean, default=False)


class SearchOrm(Base):
    __tablename__ = "search"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    query: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class UpdatesOrm(Base):
    __tablename__ = "updates"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_update_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    content: Mapped[str | None] = mapped_column(String(100), default=None)

    update_type: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    is_read: Mapped[bool | None] = mapped_column(Boolean, default=False)

    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), default=None)

    pin_id: Mapped[int | None] = mapped_column(
        ForeignKey("pins.id", ondelete="CASCADE"), default=None
    )

    comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), default=None
    )

    reply_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), default=None
    )


class UsersRecommendationsPinsOrm(Base):
    __tablename__ = "users_recommendations_pins"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    pin_id: Mapped[int] = mapped_column(ForeignKey("pins.id", ondelete="CASCADE"), nullable=False)
    update_id: Mapped[int] = mapped_column(ForeignKey("updates.id"), nullable=False)


pins_tags = Table(
    "pins_tags",
    Base.metadata,
    Column("pin_id", ForeignKey("pins.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

users_pins = Table(
    "users_pins",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("pin_id", ForeignKey("pins.id", ondelete="CASCADE"), primary_key=True),
)

board_pins = Table(
    "board_pins",
    Base.metadata,
    Column("board_id", Integer, ForeignKey("boards.id", ondelete="CASCADE"), primary_key=True),
    Column("pin_id", Integer, ForeignKey("pins.id", ondelete="CASCADE"), primary_key=True),
)

users_view_pins = Table(
    "users_view_pins",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("pin_id", ForeignKey("pins.id", ondelete="CASCADE"), primary_key=True),
)
