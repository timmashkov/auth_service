from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from infrastructure.database.models.profile import Profile
    from infrastructure.database.models.role import Role


class User(Base):

    nickname: Mapped[str] = mapped_column(
        String, unique=True, nullable=True, comment=""
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False, comment="")
    last_name: Mapped[str] = mapped_column(String, nullable=False, comment="")
    patronymic: Mapped[str] = mapped_column(String, nullable=False, comment="")
    age: Mapped[int] = mapped_column(
        Integer,
        unique=False,
        nullable=False,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    profile: Mapped["Profile"] = relationship(
        "Profile",
        backref="user",
        lazy="noload",
    )

    user_role: Mapped["Role"] = relationship(
        "Role",
        back_populates="user_link",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
