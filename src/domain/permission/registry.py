from typing import Any, List, Optional
from uuid import UUID

from asyncpg import UniqueViolationError
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain.permission.schema import CreatePermission, PermissionReturnData
from infrastructure.base_entities.abs_repository import AbstractReadRepository, AbstractWriteRepository
from infrastructure.database.alchemy_gateway import SessionManager
from infrastructure.database.models import Permission
from infrastructure.exceptions.user_exceptions import UserAlreadyExists


class PermissionReadRepository(AbstractReadRepository):

    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__()
        self.model = Permission
        self.transactional_session: async_sessionmaker = (
            session_manager.transactional_session
        )
        self.async_session_factory: async_sessionmaker = (
            session_manager.async_session_factory
        )

    async def get(self, perm_uuid: UUID) -> Optional[Permission]:
        async with self.async_session_factory() as session:
            stmt = select(self.model).filter(self.model.uuid == perm_uuid)
            answer = await session.execute(stmt)
            result = answer.scalars().unique().first()
        return result

    async def get_list(
        self,
        parameter: Any = "created_at",
    ) -> Optional[List[PermissionReturnData]]:
        async with self.async_session_factory() as session:
            final = None
            if option := getattr(self.model, parameter):
                stmt = select(self.model).order_by(option)
                result = await session.execute(stmt)
                final = result.scalars().unique().all()
        return final


class PermissionWriteRepository(AbstractWriteRepository):
    def __init__(self, session_manager: SessionManager):
        super().__init__()
        self.model = Permission
        self.transactional_session: async_sessionmaker = (
            session_manager.transactional_session
        )
        self.async_session_factory: async_sessionmaker = (
            session_manager.async_session_factory
        )

    async def create(self, cmd: CreatePermission) -> Optional[Permission]:
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
        cmd: CreatePermission,
        perm_uuid: UUID,
    ) -> Optional[Permission]:
        async with self.transactional_session() as session:
            stmt = (
                update(self.model)
                .values(**cmd.model_dump())
                .where(self.model.uuid == perm_uuid)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalars().unique().first()
        return answer

    async def delete(self, perm_uuid: UUID) -> Optional[Permission]:
        async with self.transactional_session() as session:
            stmt = (
                delete(self.model)
                .where(self.model.uuid == perm_uuid)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            answer = result.scalars().unique().first()
        return answer
