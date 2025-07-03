import asyncio

from broker.config.preferences import USER_SERVER, NEW_USER_TOPIC
from broker.consumers.user_consumer import UserConsumer


async def main():
    consumer = UserConsumer(
        kafka_servers=USER_SERVER,
        topic=NEW_USER_TOPIC
    )
    await consumer.consume()


if __name__ == '__main__':
    asyncio.run(main())
