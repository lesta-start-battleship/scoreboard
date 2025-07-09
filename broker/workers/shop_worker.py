import asyncio

from broker.config.preferences import KAFKA_SERVER, CHEST_OPEN_TOPIC
from broker.config.telemetry import setup_broker_telemetry
from broker.consumers.shop_consumer import ShopConsumer

setup_broker_telemetry(app_name="scoreboard-shop-worker-broker", app_version="0.1.0")


async def main():
    consumer_action_chest_open = ShopConsumer(KAFKA_SERVER, CHEST_OPEN_TOPIC)

    await consumer_action_chest_open.consume()


if __name__ == '__main__':
    asyncio.run(main())
