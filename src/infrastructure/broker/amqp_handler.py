import asyncio
from multiprocessing import Process

from application.container import Container
from infrastructure.broker.kafka import KafkaConsumer


async def _amqp_handler(
    kafka_client: KafkaConsumer = Container.consumer_client(),
) -> None:
    await kafka_client.connect()


def amqp_handler():
    _loop = asyncio.get_event_loop()
    _loop.run_until_complete(_amqp_handler())
    _loop.run_forever()


amqp_process = Process(target=amqp_handler)
