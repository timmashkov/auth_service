from typing import Any, List, Optional
from uuid import UUID

from asyncpg import UniqueViolationError
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.role.schema import CreateRole, RoleReturnData
from infrastructure.base_entities.abs_repository import (
    AbstractReadRepository,
    AbstractWriteRepository,
)
from infrastructure.database.alchemy_gateway import SessionManager
from infrastructure.database.models import Role
from infrastructure.exceptions.user_exceptions import UserAlreadyExists


class RoleReadRepository(AbstractReadRepository):

    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__()
        self.model = Role
        self.transactional_session: async_sessionmaker = (
            session_manager.transactional_session
        )
        self.async_session_factory: async_sessionmaker = (
            session_manager.async_session_factory
        )

    async def get(self, role_uuid: UUID) -> Optional[Role]:
        async with self.async_session_factory() as session:
            stmt = select(self.model).filter(self.model.uuid == role_uuid)
            answer = await session.execute(stmt)
            result = answer.scalars().unique().first()
        return result

    async def get_list(
        self,
        parameter: Any = "created_at",
    ) -> Optional[List[RoleReturnData]]:
        async with self.async_session_factory() as session:
            final = None
            if option := getattr(self.model, parameter):
                stmt = select(self.model).order_by(option)
                result = await session.execute(stmt)
                final = result.scalars().unique().all()
        return final


class RoleWriteRepository(AbstractWriteRepository):
    def __init__(self, session_manager: SessionManager):
        super().__init__()
        self.model = Role
        self.transactional_session: async_sessionmaker = (
            session_manager.transactional_session
        )
        self.async_session_factory: async_sessionmaker = (
            session_manager.async_session_factory
        )

    async def create(self, cmd: CreateRole) -> Optional[Role]:
        try:
            async with self.transactional_session() as session:
                stmt = (
                    insert(self.model).values(**cmd.model_dump()).returning(self.model)
                )
                result = await session.execute(stmt)
                await session.commit()
                answer = result.scalars().unique().first()
            return answer
        except (UniqueViolationError, IntegrityError):
            raise UserAlreadyExists

    async def update(
        self,
        cmd: CreateRole,
        role_uuid: UUID,
    ) -> Optional[Role]:
        async with self.transactional_session() as session:
            stmt = (
                update(self.model)
                .values(**cmd.model_dump())
                .where(self.model.uuid == role_uuid)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalars().unique().first()
        return answer

    async def delete(self, role_uuid: UUID) -> Optional[Role]:
        async with self.transactional_session() as session:
            stmt = (
                delete(self.model)
                .where(self.model.uuid == role_uuid)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalars().unique().first()
        return answer
