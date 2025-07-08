import asyncio

from broker.config.preferences import KAFKA_SERVER, CORE_MATCH_END_TOPIC
from broker.consumers.core_consumer import CoreConsumer
from broker.producers.guild_war_produser import start_producer, stop_producer


async def main():
    await start_producer()

    consumer_match = CoreConsumer(KAFKA_SERVER, CORE_MATCH_END_TOPIC)

    await consumer_match.consume()

    await stop_producer()


if __name__ == '__main__':
    asyncio.run(main())
