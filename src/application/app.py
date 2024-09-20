from application.config import settings
from infrastructure.server.server import Server

auth_service = Server(
    name=settings.NAME,
    routers=[],
    start_callbacks=[],
    stop_callbacks=[],
).app
