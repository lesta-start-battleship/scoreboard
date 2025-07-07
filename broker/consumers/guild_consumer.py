from aiokafka import AIOKafkaConsumer
from pydantic_core._pydantic_core import ValidationError

from broker.config.preferences import GUILD_CREATE_TOPIC, GUILD_DELETE_TOPIC, GUILD_MEMBER_CHANGE_TOPIC
from broker.schemas.guild.guild_create import GuildCreateDTO
from broker.schemas.guild.guild_delete import GuildDeleteDTO
from broker.schemas.guild.guild_member_change import GuildMemberChangeDTO
from shared.database.database import async_session
from shared.repositories.guild import create_guild, delete_guild, update_guild


class GuildConsumer:
    def __init__(self, kafka_servers: str, topic: str):
        self.topic = topic
        self.kafka_servers = kafka_servers
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.kafka_servers,
            group_id="scoreboard.guild.consumer"
        )

    async def consume(self):
        await self.consumer.start()
        try:

            async for message in self.consumer:
                try:

                    if self.topic == GUILD_CREATE_TOPIC:
                        data = GuildCreateDTO.model_validate_json(message.value)
                        await self.handle_new_guild(data)

                    elif self.topic == GUILD_DELETE_TOPIC:
                        data = GuildDeleteDTO.model_validate_json(message.value)
                        await self.handle_delete_guild(data)

                    elif self.topic == GUILD_MEMBER_CHANGE_TOPIC:
                        data = GuildMemberChangeDTO.model_validate_json(message.value)
                        await self.handle_member_change_guild(data)

                    await self.consumer.commit()

                except ValidationError as e:
                    print(f"Ошибка валидации данных: {e}")

        finally:
            await self.consumer.stop()

    async def handle_new_guild(self, data: GuildCreateDTO):
        async with async_session() as session:
            new_guild = data.model_dump()
            await create_guild(session, **new_guild)

    async def handle_delete_guild(self, data: GuildDeleteDTO):
        async with async_session() as session:
            data = data.model_dump()
            await delete_guild(session, **data)

    async def handle_member_change_guild(self, data: GuildMemberChangeDTO):
        async with async_session() as session:
            data = data.model_dump()
            await update_guild(session, **data)
