from application.config import settings
from application.container import Container
from infrastructure.server.server import Server
from presentation.user import UserRouter

auth_service = Server(
    name=settings.NAME,
    routers=[UserRouter().api_router],
    start_callbacks=[],
    stop_callbacks=[Container.redis().close],
).app
