import asyncio

from broker.config.preferences import KAFKA_SERVER, CORE_MATCH_END_TOPIC, GUILD_WAR_END_TOPIC
from broker.consumers.core_consumer import CoreConsumer
from broker.producers.guild_war_produser import GuildWarProducer


async def main():
    producer_match = GuildWarProducer(KAFKA_SERVER, GUILD_WAR_END_TOPIC)
    await producer_match.start_producer()
    consumer_match = CoreConsumer(KAFKA_SERVER, CORE_MATCH_END_TOPIC, producer_match)
    try:
        await consumer_match.consume()
    finally:
        await producer_match.stop_producer()


if __name__ == '__main__':
    asyncio.run(main())
