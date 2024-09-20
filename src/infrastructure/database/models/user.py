from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.base_entities.base_table import Base


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
