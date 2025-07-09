import json

from aiokafka import AIOKafkaConsumer
from opentelemetry.trace import Status, StatusCode
from pydantic_core import ValidationError

from broker.config.logger import setup_logger
from broker.config.preferences import GUILD_WAR_END_TOPIC
from broker.enums.match import MatchType as mt
from broker.producers.guild_war_produser import GuildWarProducer
from broker.schemas.match.custom import MatchCustomDTO
from broker.schemas.match.guild_war import MatchGuildWarDTO
from broker.schemas.match.guild_war_respone import GuildWarResponseDTO
from broker.schemas.match.random import MatchRandomDTO
from broker.schemas.match.ranked import MatchRankedDTO
from shared.database.database import async_session
from shared.repositories.guild import update_guild
from shared.repositories.user import update_user
from shared.repositories.war_result import update_war_result

logger = setup_logger("core_consumer")


class CoreConsumer:
    def __init__(self, kafka_servers: str, topic: str, producer: GuildWarProducer):
        self.kafka_servers = kafka_servers
        self.topic = topic
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=kafka_servers,
            group_id="scoreboard.core.consumer"
        )
        self.producer = producer

    async def consume(self):
        await self.consumer.start()
        logger.info(f"CoreConsumer started consume topic {self.topic}")
        try:

            async for message in self.consumer:
                with get_tracer(__name__).start_as_current_span("consume_core_message") as span:
                    try:
                        match_type: str = json.loads(message.value)["match_type"]
                        if match_type == mt.RANDOM.value:
                            data = MatchRandomDTO.model_validate_json(message.value)
                            logger.debug(f"**RANDOM** MatchRandomDTO {data}")
                            await self.handle_random_match(data)
                        elif match_type == mt.RANKED.value:
                            data = MatchRankedDTO.model_validate_json(message.value)
                            logger.debug(f"**RANKED** MatchRankedDTO {data}")
                            await self.handle_ranked_match(data)
                        elif match_type == mt.CUSTOM.value:
                            data = MatchCustomDTO.model_validate_json(message.value)
                            logger.debug(f"**CUSTOM** MatchCustomDTO {data}")
                            await self.handle_custom_match(data)
                        elif match_type == mt.GUILD_WAR_MATCH.value:
                            data = MatchGuildWarDTO.model_validate_json(message.value)
                            logger.debug(f"**GUILD WAR** MatchGuildWarDTO {data}")
                            await self.handle_guild_war_match(data)
                        else:
                            raise ValueError(f"Unknown match type {match_type}")

                        await self.consumer.commit()

                    except ValidationError as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                        logger.error(f"Validation error: {e}")

        finally:
            await self.consumer.stop()

    async def handle_random_match(self, data: MatchRandomDTO):
        async with async_session() as session:
            try:
                await update_user(
                    session=session,
                    user_id=data.winner_match_id,
                    experience=data.experience.winner_gain
                )

                await update_user(
                    session=session,
                    user_id=data.loser_match_id,
                    experience=data.experience.loser_gain
                )
            except ValueError:
                pass

    async def handle_ranked_match(self, data: MatchRankedDTO):
        async with async_session() as session:
            try:
                await update_user(
                    session=session,
                    user_id=data.winner_match_id,
                    experience=data.experience.winner_gain,
                    rating=data.rating.winner_gain
                )

                await update_user(
                    session=session,
                    user_id=data.loser_match_id,
                    experience=data.experience.loser_gain,
                    rating=data.rating.loser_gain
                )
            except ValueError:
                pass

    async def handle_custom_match(self, data: MatchCustomDTO):
        logger.info(f"Custom match\nWinner {data.winner_match_id}\nLoser {data.loser_match_id}\nNo experience gained")

    async def handle_guild_war_match(self, data: MatchGuildWarDTO):
        async with async_session() as session:
            match_data = data.model_dump(include={"war_id", "winner_match_id"})
            logger.debug(f"**GUILD WAR** MatchGuildWarDTO.model_dump {match_data}")

            try:
                war_res = await update_war_result(session, **match_data)

                attacker_score = war_res.attacker_score
                defender_score = war_res.defender_score

                if attacker_score + defender_score >= 5:
                    winner_war_id = war_res.attacker_id if attacker_score > defender_score else war_res.defender_id
                    loser_war_id = war_res.attacker_id if attacker_score < defender_score else war_res.defender_id

                    war_res = await update_war_result(
                        session=session,
                        war_id=war_res.war_id,
                        winner_war_id=winner_war_id,
                        loser_war_id=loser_war_id
                    )
                    await update_guild(
                        session=session,
                        guild_id=winner_war_id,
                        wins=1
                    )

                    message = GuildWarResponseDTO(
                        id_guild_attacker=war_res.attacker_id,
                        score_attacker=war_res.attacker_score,
                        id_guild_defender=war_res.defender_id,
                        score_defender=war_res.defender_score,
                        id_winner=war_res.winner_id,
                        id_guild_war=war_res.war_id,
                        correlation_id=war_res.correlation_id
                    )
                    await self.producer.send_guild_war_end_message(GUILD_WAR_END_TOPIC, message)
            except ValueError:
                pass
