import asyncio
import logging
from typing import Optional, Union
from uuid import UUID

from sqlalchemy import delete, insert, update

from application.container import Container
from domain.user.registry import UserReadRepository
from domain.user.schema import CreateUser, UpdateUser
from infrastructure.broker.kafka import KafkaProducer
from infrastructure.config.config import settings
from infrastructure.database.alchemy_gateway import SessionManager
from infrastructure.database.models import User


async def create_profile_on_event(
    event_type: str,
    user_uuid: Optional[Union[UUID, str]],
    user_data: Optional[Union[CreateUser, UpdateUser]] = None,
    kafka_client: KafkaProducer = Container.producer_client(),
    read_client: UserReadRepository = Container.user_read_repository(),
    session_manager: SessionManager = Container.alchemy_manager(),
) -> None:
    """
    Таска создания профиля при ивенте юзера
    """
    user = await read_client.get(user_uuid=user_uuid)
    data_dict = user_data.model_dump() if user_data else {}
    data_dict["event_type"] = event_type
    async with session_manager.async_session_factory() as session:
        if event_type == "create" and not user:
            data_dict["uuid"] = user.uuid
            stmt = insert(User).values(**user_data)
            try:
                asyncio.create_task(
                    kafka_client.simple_send_message(
                        message=data_dict,
                        topic=settings.KAFKA.topics.register_topic,
                    ),
                )
                asyncio.create_task(session.execute(stmt))
            except Exception as e:
                await session.rollback()
                logging.error(f"Ошибка при создании записи: {e}")
        elif event_type == "update" and user:
            data_dict = user_data.model_dump()
            data_dict["uuid"] = user.uuid
            stmt = update(User).values(**user_data).where(User.uuid == user_uuid)
            try:
                asyncio.create_task(
                    kafka_client.transactional_send_message(
                        message=data_dict,
                        topic=settings.KAFKA.topics.register_topic,
                    ),
                )
                asyncio.create_task(session.execute(stmt))
            except Exception as e:
                await session.rollback()
                logging.error(f"Ошибка при обновлении записи записи: {e}")
        elif event_type == "delete" and user:
            data_dict["uuid"] = user.uuid
            stmt = delete(User).where(User.uuid == user_uuid)
            try:
                asyncio.create_task(
                    kafka_client.transactional_send_message(
                        message=data_dict,
                        topic=settings.KAFKA.topics.register_topic,
                    ),
                )
                asyncio.create_task(session.execute(stmt))
            except Exception as e:
                await session.rollback()
                logging.error(f"Ошибка при удалении записи записи: {e}")
        await session.commit()
