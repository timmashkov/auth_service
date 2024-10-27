from asyncio import run
from multiprocessing import Process
from typing import Coroutine

from application.tasks.clickhouse_table_creation import create_tables_task
from application.tasks.data_sync_task import synchronization_task
from infrastructure.config.config import settings
from infrastructure.utils.asyncio.asyncio_handlers import safe_gather, start_task


async def _start_background_tasks():
    tasks: list[Coroutine] = [
        start_task(create_tables_task(), settings.REPEAT_TIMEOUT),
        start_task(synchronization_task(), settings.REPEAT_TIMEOUT),
    ]
    await safe_gather(*tasks)


def start_background_tasks():
    run(_start_background_tasks())


background_process = Process(target=start_background_tasks)
