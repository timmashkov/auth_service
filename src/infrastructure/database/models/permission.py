from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from infrastructure.database.models.role import Role


class Permission(Base):

    name: Mapped[str] = mapped_column(
        String, comment="Человекочитаемое название разрешения"
    )
    layer: Mapped[str] = mapped_column(
        String, comment="К чему относится разрешение ('frontend'/'backend'/...)"
    )
    jdata: Mapped[dict] = mapped_column(
        JSONB, server_default="{}", default={}, comment="Разрешения"
    )

    role_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("roles.uuid", ondelete="CASCADE"), unique=True, nullable=True
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="role_permissions",
        lazy="noload",
    )
