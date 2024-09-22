from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from infrastructure.database.models.role import Role


class User(Base):

    nickname: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )
    login: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    age: Mapped[int] = mapped_column(
        Integer,
        unique=False,
        nullable=False,
    )
    phone_number: Mapped[str] = mapped_column(
        String(11),
        unique=True,
        nullable=False,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    user_role: Mapped["Role"] = relationship(
        "Role",
        back_populates="user_link",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
