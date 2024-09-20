from application.config import settings
from infrastructure.base_entities.singleton import OnlyContainer, Singleton
from infrastructure.database.alchemy_gateway import SessionManager


class Container(Singleton):

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
