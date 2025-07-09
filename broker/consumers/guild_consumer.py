from aiokafka import AIOKafkaConsumer
from opentelemetry.trace import Status, StatusCode
from pydantic_core._pydantic_core import ValidationError

from broker.config.logger import setup_logger
from broker.config.preferences import (
    GUILD_CREATE_TOPIC,
    GUILD_DELETE_TOPIC,
    GUILD_MEMBER_CHANGE_TOPIC,
    GUILD_START_GUILD_WAR_TOPIC
)
from broker.config.telemetry import get_tracer
from broker.schemas.guild.guild_create import GuildCreateDTO
from broker.schemas.guild.guild_delete import GuildDeleteDTO
from broker.schemas.guild.guild_member_change import GuildMemberChangeDTO
from broker.schemas.guild.guild_war import GuildWarDTO
from shared.database.database import async_session
from shared.repositories.guild import create_guild, delete_guild, update_guild
from shared.repositories.user import update_user
from shared.repositories.war_result import create_war_result

logger = setup_logger("user_consumer")


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
        logger.info(f"GuildConsumer started consume topic {self.topic}")
        try:

            async for message in self.consumer:
                with get_tracer(__name__).start_as_current_span("consume_guild_message") as span:
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

                        elif self.topic == GUILD_START_GUILD_WAR_TOPIC:
                            data = GuildWarDTO.model_validate_json(message.value)
                            await self.handle_start_guild_war(data)

                        await self.consumer.commit()

                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                        logger.error(f"Validation error: {e}")

        finally:
            await self.consumer.stop()
            logger.info("GuildConsumer stopped")

    async def handle_new_guild(self, data: GuildCreateDTO):
        async with async_session() as session:
            new_guild = data.model_dump(exclude={"user_owner_id"})
            logger.debug(f"**NEW GUILD** GuildCreateDTO.model_dump {new_guild}")
            await create_guild(session, **new_guild)
            await update_user(session, user_id=data.user_owner_id, guild_id=data.guild_id)

    async def handle_delete_guild(self, data: GuildDeleteDTO):
        async with async_session() as session:
            try:
                data = data.model_dump()
                logger.debug(f"**DELETE GUILD** GuildDeleteDTO.model_dump {data}")
                await delete_guild(session, **data)
            except ValueError:
                pass

    async def handle_member_change_guild(self, data: GuildMemberChangeDTO):
        async with async_session() as session:
            try:
                guild_data = data.model_dump(include={"guild_id", "players"})
                logger.debug(f"**MEMBER CHANGE GUILD** GuildMemberChangeDTO.model_dump {data}")
                await update_guild(session, **guild_data)
                await update_user(
                    session=session,
                    user_id=data.user_id,
                    guild_id=data.guild_id,
                    leaving_guild=not bool(data.action)
                )
            except ValueError:
                pass

    async def handle_start_guild_war(self, data: GuildWarDTO):
        async with async_session() as session:
            try:
                data = data.model_dump()
                logger.debug(f"**GUILD WAR** GuildWarDTO.model_dump {data}")
                await create_war_result(session, **data)
            except Exception:
                logger.error("Some error occurred")