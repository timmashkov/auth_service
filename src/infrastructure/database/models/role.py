from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from infrastructure.database.models.permission import Permission
    from infrastructure.database.models.user import User


class Role(Base):

    name: Mapped[str] = mapped_column(String, unique=True, comment="Название")

    jdata: Mapped[dict] = mapped_column(
        JSONB, server_default="{}", default={}, comment="Дополнительные данные"
    )

    user_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE"), unique=True, nullable=True
    )

    user_link: Mapped["User"] = relationship(
        "User",
        back_populates="user_role",
        lazy="noload",
    )

    role_permissions: Mapped["Permission"] = relationship(
        "Permission",
        back_populates="role",
        lazy="noload",
        cascade="all, delete-orphan",
        passive_updates=True,
        passive_deletes=True,
        single_parent=True,
    )
