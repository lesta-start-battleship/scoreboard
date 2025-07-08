import asyncio

from broker.config.preferences import KAFKA_SERVER, CORE_MATCH_END_TOPIC, GUILD_WAR_END_TOPIC
from broker.config.telemetry import setup_broker_telemetry
from broker.consumers.core_consumer import CoreConsumer
from broker.producers.guild_war_produser import GuildWarProducer

setup_broker_telemetry(app_name="scoreboard-game-worker-broker", app_version="0.1.0")

async def main():
    producer_game = GuildWarProducer(KAFKA_SERVER, GUILD_WAR_END_TOPIC)
    await producer_game.start_producer()
    consumer_match = CoreConsumer(KAFKA_SERVER, CORE_MATCH_END_TOPIC, producer_game)
    try:
        await consumer_match.consume()
    finally:
        await producer_game.stop_producer()


if __name__ == '__main__':
    asyncio.run(main())
