import asyncio

from broker.config.preferences import (
    KAFKA_SERVER,
    GUILD_CREATE_TOPIC,
    GUILD_DELETE_TOPIC,
    GUILD_MEMBER_CHANGE_TOPIC, GUILD_START_GUILD_WAR_TOPIC
)
from broker.config.telemetry import setup_broker_telemetry
from broker.consumers.guild_consumer import GuildConsumer

setup_broker_telemetry(app_name="scoreboard-guild-worker-broker", app_version="0.1.0")


async def main():
    consumer_guild_create = GuildConsumer(KAFKA_SERVER, GUILD_CREATE_TOPIC)
    consumer_guild_delete = GuildConsumer(KAFKA_SERVER, GUILD_DELETE_TOPIC)
    consumer_guild_member_change = GuildConsumer(KAFKA_SERVER, GUILD_MEMBER_CHANGE_TOPIC)
    consumer_guild_war_start = GuildConsumer(KAFKA_SERVER, GUILD_START_GUILD_WAR_TOPIC)

    task1 = asyncio.create_task(consumer_guild_create.consume())
    task2 = asyncio.create_task(consumer_guild_delete.consume())
    task3 = asyncio.create_task(consumer_guild_member_change.consume())
    task4 = asyncio.create_task(consumer_guild_war_start.consume())

    await asyncio.gather(task1, task2, task3, task4)


if __name__ == '__main__':
    asyncio.run(main())
