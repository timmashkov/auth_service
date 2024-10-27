import asyncio
import logging
from typing import Type

from sqlalchemy import select

from application.container import Container
from infrastructure.database.alchemy_gateway import SessionManager
from infrastructure.database.clickhouse_gateway import ClickHouseManager
from infrastructure.database.models import Base, Permission, Role, RolePermission, User, UserRole
from infrastructure.utils.asyncio.asyncio_handlers import safe_gather


async def postgres_clickhouse_sync(
    table: Type[Base],
    alchemy_manager: SessionManager = Container.alchemy_manager(),
    clickhouse_manager: ClickHouseManager = Container.clickhouse_manager(),
) -> None:
    logging.info(f"Start data sync in the table {table.__tablename__}")
    try:
        async with alchemy_manager.async_session_factory() as session:
            stmt = select(table).order_by(table.created_at)
            answer = await session.execute(stmt)
            all_data = answer.mappings().all()
        await safe_gather(
            *[
                clickhouse_manager.insert_object(
                    table=str(table.__tablename__),
                    data=data,
                )
                for data in all_data
            ],
        )
        logging.info("Synchronization has been completed")
    except Exception as e:
        logging.error(f"Error while synchronization: {e}")


async def synchronization_task() -> list[asyncio.Task]:
    tables = [User, Role, Permission, RolePermission, UserRole]
    return [asyncio.create_task(postgres_clickhouse_sync(table)) for table in tables]
