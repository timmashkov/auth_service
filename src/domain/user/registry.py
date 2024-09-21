from typing import Any, List, Optional
from uuid import UUID

from asyncpg import UniqueViolationError
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.user.schema import UserReturnData
from infrastructure.base_entities.abs_repository import (
    AbstractReadRepository,
    AbstractWriteRepository,
)
from infrastructure.database.alchemy_gateway import SessionManager
from infrastructure.database.models import User
from infrastructure.exceptions.user_exceptions import UserAlreadyExists


class UserReadRepository(AbstractReadRepository):

    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__()
        self.model = User
        self.transactional_session: async_sessionmaker = (
            session_manager.transactional_session
        )
        self.async_session_factory: async_sessionmaker = (
            session_manager.async_session_factory
        )

    async def get(self, user_uuid: UUID) -> Optional[UserReturnData]:
        async with self.async_session_factory() as session:
            stmt = select(self.model).filter(self.model.uuid == user_uuid)
            answer = await session.execute(stmt)
            result = answer.scalar_one_or_none()
        return result

    async def get_by_nickname(self, nickname: str) -> Optional[UserReturnData]:
        async with self.async_session_factory() as session:
            stmt = select(self.model).filter(self.model.nickname == nickname)
            answer = await session.execute(stmt)
            result = answer.scalar_one_or_none()
        return result

    async def get_list(
        self,
        parameter: Any = "created_at",
    ) -> Optional[List[UserReturnData]]:
        async with self.async_session_factory() as session:
            final = None
            if option := getattr(self.model, parameter):
                stmt = select(self.model).order_by(option)
                result = await session.execute(stmt)
                final = result.scalars().all()
        return final


class UserWriteRepository(AbstractWriteRepository):
    def __init__(self, session_manager: SessionManager):
        super().__init__()
        self.model = User
        self.transactional_session: async_sessionmaker = (
            session_manager.transactional_session
        )
        self.async_session_factory: async_sessionmaker = (
            session_manager.async_session_factory
        )

    async def create(self, cmd: Any) -> Optional[User]:
        try:
            async with self.transactional_session() as session:
                stmt = (
                    insert(self.model).values(**cmd.model_dump()).returning(self.model)
                )
                result = await session.execute(stmt)
                await session.commit()
                answer = result.scalar_one_or_none()
            return answer
        except (UniqueViolationError, IntegrityError):
            raise UserAlreadyExists

    async def update(
        self,
        cmd: Any,
        user_uuid: UUID,
    ) -> Optional[User]:
        async with self.transactional_session() as session:
            stmt = (
                update(self.model)
                .values(**cmd.model_dump())
                .where(self.model.uuid == user_uuid)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalar_one_or_none()
        return answer

    async def delete(self, user_uuid: UUID) -> Optional[User]:
        async with self.transactional_session() as session:
            stmt = (
                delete(self.model)
                .where(self.model.uuid == user_uuid)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalar_one_or_none()
        return answer
