import asyncio

from broker.config.preferences import (
    KAFKA_SERVER,
    GUILD_CREATE_TOPIC,
    GUILD_DELETE_TOPIC,
    GUILD_MEMBER_CHANGE_TOPIC
)
from broker.consumers.guild_consumer import GuildConsumer


async def main():
    consumer_guild_create = GuildConsumer(KAFKA_SERVER, GUILD_CREATE_TOPIC)
    consumer_guild_delete = GuildConsumer(KAFKA_SERVER, GUILD_DELETE_TOPIC)
    consumer_guild_member_change = GuildConsumer(KAFKA_SERVER, GUILD_MEMBER_CHANGE_TOPIC)

    task1 = asyncio.create_task(consumer_guild_create.consume())
    task2 = asyncio.create_task(consumer_guild_delete.consume())
    task3 = asyncio.create_task(consumer_guild_member_change.consume())

    await asyncio.gather(task1, task2, task3)


if __name__ == '__main__':
    asyncio.run(main())
