from sqlalchemy import Boolean, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.base_entities.base_table import Base


class Role(Base):

    name: Mapped[str] = mapped_column(String, unique=True, comment="Название")
    jdata: Mapped[dict] = mapped_column(
        JSONB, server_default="{}", default={}, comment="Дополнительные данные"
    )
