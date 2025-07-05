import asyncio

from broker.config.preferences import KAFKA_SERVER, CHEST_OPEN_TOPIC
from broker.consumers.shop_consumer import ShopConsumer


async def main():
    consumer_action_chest_open = ShopConsumer(KAFKA_SERVER, CHEST_OPEN_TOPIC)

    await consumer_action_chest_open.consume()


if __name__ == '__main__':
    asyncio.run(main())
