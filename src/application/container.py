from redis.asyncio import Redis

from domain.permission.registry import PermissionReadRepository, PermissionWriteRepository
from domain.role.registry import RoleReadRepository, RoleWriteRepository
from domain.user.registry import UserReadRepository, UserWriteRepository
from infrastructure.auth.token_handler import AuthHandler
from infrastructure.base_entities.singleton import OnlyContainer, Singleton
from infrastructure.broker.kafka import KafkaConsumer, KafkaProducer
from infrastructure.config.config import settings
from infrastructure.database.alchemy_gateway import SessionManager
from infrastructure.database.clickhouse_gateway import ClickHouseManager


class Container(Singleton):

    redis = OnlyContainer(
        Redis,
        **settings.REDIS,
        decode_responses=True,
    )

    alchemy_manager = OnlyContainer(
        SessionManager,
        dialect=settings.POSTGRES.dialect,
        host=settings.POSTGRES.host,
        login=settings.POSTGRES.login,
        password=settings.POSTGRES.password,
        port=settings.POSTGRES.port,
        database=settings.POSTGRES.database,
        echo=settings.POSTGRES.echo,
    )

    clickhouse_manager = OnlyContainer(
        ClickHouseManager,
        host=settings.CLICKHOUSE.host,
        user=settings.CLICKHOUSE.user,
        password=settings.CLICKHOUSE.password,
        port=settings.CLICKHOUSE.port,
        database=settings.CLICKHOUSE.database,
    )

    user_read_repository = OnlyContainer(
        UserReadRepository,
        session_manager=alchemy_manager(),
    )

    user_write_repository = OnlyContainer(
        UserWriteRepository,
        session_manager=alchemy_manager(),
    )

    role_read_repository = OnlyContainer(
        RoleReadRepository,
        session_manager=alchemy_manager(),
    )

    role_write_repository = OnlyContainer(
        RoleWriteRepository,
        session_manager=alchemy_manager(),
    )

    perm_read_repository = OnlyContainer(
        PermissionReadRepository,
        session_manager=alchemy_manager(),
    )

    perm_write_repository = OnlyContainer(
        PermissionWriteRepository,
        session_manager=alchemy_manager(),
    )

    auth_handler = OnlyContainer(
        AuthHandler,
        secret=settings.AUTH.secret,
        exp=settings.AUTH.expiration,
        api_x_key_header=settings.AUTH.api_x_key_header,
        iterations=settings.AUTH.iterations,
        hash_name=settings.AUTH.hash_name,
        formats=settings.AUTH.formats,
        algorythm=settings.AUTH.algorythm,
        redis_client=redis(),
    )

    producer_client = OnlyContainer(
        KafkaProducer,
        host=settings.KAFKA.host,
        port=settings.KAFKA.port,
        topics=settings.KAFKA.topics,
        logging_config=settings.LOG_LEVEL,
        acks=settings.KAFKA.acks,
        transactional_id=settings.KAFKA.transactional_id,
    )

    consumer_client = OnlyContainer(
        KafkaConsumer,
        host=settings.KAFKA.host,
        port=settings.KAFKA.port,
        topics=[settings.KAFKA.topics.register_topic],
        logging_config=settings.LOG_LEVEL,
    )
