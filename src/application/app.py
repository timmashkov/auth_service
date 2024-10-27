from application.background import background_process
from application.container import Container
from infrastructure.broker.amqp_handler import amqp_process
from infrastructure.config.config import settings
from infrastructure.server.server import Server
from presentation.auth import AuthRouter
from presentation.permission import PermissionRouter
from presentation.role import RoleRouter
from presentation.user import UserRouter

auth_service = Server(
    name=settings.NAME,
    routers=[
        UserRouter().api_router,
        RoleRouter().api_router,
        PermissionRouter().api_router,
        AuthRouter().api_router,
    ],
    start_callbacks=[
        amqp_process.start,
        background_process.start,
        Container.producer_client().connect,
        Container.consumer_client().connect,
    ],
    stop_callbacks=[
        Container.redis().close,
        Container.producer_client().disconnect,
        Container.consumer_client().disconnect,
        amqp_process.close,
        background_process.close,
    ],
).app
