from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from infrastructure.database.models.user import User


class Profile(Base):

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

    user_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE"), unique=True, nullable=True
    )

    # user: Mapped["User"] = relationship(
    #     "User",
    #     backref="profile",
    #     lazy="noload",
    #     cascade="all, delete-orphan",
    #     passive_updates=True,
    #     passive_deletes=True,
    #     single_parent=True,
    # )
