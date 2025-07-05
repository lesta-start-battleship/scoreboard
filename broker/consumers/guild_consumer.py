from aiokafka import AIOKafkaConsumer
from pydantic_core._pydantic_core import ValidationError

from broker.config.preferences import GUILD_CREATE_TOPIC, GUILD_DELETE_TOPIC, GUILD_MEMBER_CHANGE_TOPIC
from broker.schemas.guild.guild_create import GuildCreateDTO
from broker.schemas.guild.guild_delete import GuildDeleteDTO
from broker.schemas.guild.guild_member_change import GuildMemberChangeDTO


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
                        user_data = GuildCreateDTO.model_validate_json(message.value)
                        pass

                    elif self.topic == GUILD_DELETE_TOPIC:
                        user_data = GuildDeleteDTO.model_validate_json(message.value)
                        pass

                    elif self.topic == GUILD_MEMBER_CHANGE_TOPIC:
                        user_data = GuildMemberChangeDTO.model_validate_json(message.value)
                        pass

                    await self.consumer.commit()

                except ValidationError as e:
                    print(f"Ошибка валидации данных: {e}")

        finally:
            await self.consumer.stop()
