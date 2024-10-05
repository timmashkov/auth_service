from application.config import settings
from application.container import Container
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
    start_callbacks=[],
    stop_callbacks=[
        Container.redis().close,
        Container.producer_client().disconnect,
        Container.consumer_client().disconnect,
    ],
).app
