from aiokafka import AIOKafkaConsumer
from opentelemetry.trace import Status, StatusCode
from pydantic_core._pydantic_core import ValidationError

from broker.config.logger import setup_logger
from broker.config.preferences import NEW_USER_TOPIC, USERNAME_CHANGE_TOPIC, CURRENCY_CHANGE_TOPIC
from broker.config.telemetry import get_tracer
from broker.schemas.user.currency_change import CurrencyChangeDTO
from broker.schemas.user.new_user import NewUserDTO
from broker.schemas.user.username_change import UsernameChangeDTO
from shared.database.database import async_session
from shared.repositories.user import create_user, update_user

logger = setup_logger("user_consumer")


class UserConsumer:
    def __init__(self, kafka_servers: str, topic: str):
        self.topic = topic
        self.kafka_servers = kafka_servers
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.kafka_servers,
            group_id="scoreboard.user.consumer"
        )

    async def consume(self):
        await self.consumer.start()
        logger.info(f"UserConsumer started consume topic {self.topic}")
        try:

            async for message in self.consumer:
                with get_tracer(__name__).start_as_current_span("consume_user_message") as span:
                    try:
                        if self.topic == NEW_USER_TOPIC:
                            user_data = NewUserDTO.model_validate_json(message.value)
                            await self.handle_new_user(user_data)

                        elif self.topic == USERNAME_CHANGE_TOPIC:
                            user_data = UsernameChangeDTO.model_validate_json(message.value)
                            await self.handle_username_change(user_data)

                        elif self.topic == CURRENCY_CHANGE_TOPIC:
                            user_data = CurrencyChangeDTO.model_validate_json(message.value)
                            await self.handle_currency_change(user_data)

                        await self.consumer.commit()
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                        logger.error(f"Validation error: {e}")

        finally:
            await self.consumer.stop()
            logger.info("UserConsumer stopped")

    async def handle_new_user(self, user_data: NewUserDTO):
        async with async_session() as session:
            try:
                new_user = user_data.model_dump()
                logger.debug(f"**NEW USERNAME** UsernameChangeDTO.model_dump {new_user}")
                await create_user(session, **new_user)
            except Exception:
                raise
    async def handle_username_change(self, user_data: UsernameChangeDTO):
        async with async_session() as session:
            try:
                new_user_data = user_data.model_dump()
                logger.debug(f"**USERNAME CHANGE** UsernameChangeDTO.model_dump {new_user_data}")
                await update_user(session, **new_user_data)
            except AttributeError:
                logger.error(f"**USERNAME CHANGE** user with user_id={user_data.user_id} does not exists in db")
                pass
            except ValueError:
                pass
            except Exception:
                logger.error(f"**USERNAME CHANGE** some problems")
                pass

    async def handle_currency_change(self, user_data: CurrencyChangeDTO):
        async with async_session() as session:
            try:
                new_user_data = user_data.model_dump()
                logger.debug(f"**CURRENCY CHANGE** CurrencyChangeDTO.model_dump {new_user_data}")
                await update_user(session, **new_user_data)
            except AttributeError:
                logger.error(f"**CURRENCY CHANGE** user with user_id={user_data.user_id} does not exists in db")
                pass
            except ValueError:
                pass
            except Exception:
                logger.error(f"**USERNAME CHANGE** some problems")
                pass
