from aiokafka import AIOKafkaConsumer
from opentelemetry.trace import Status, StatusCode
from pydantic_core._pydantic_core import ValidationError

from broker.config.logger import setup_logger
from broker.config.telemetry import get_tracer
from broker.schemas.shop.action_chest_open import ActionChestOpenDTO
from shared.database.database import async_session
from shared.repositories.user import update_user

logger = setup_logger("shop_consumer")

class ShopConsumer:
    def __init__(self, kafka_servers: str, topic: str):
        self.topic = topic
        self.kafka_servers = kafka_servers
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.kafka_servers,
            group_id="scoreboard.shop.consumer"
        )

    async def consume(self):
        await self.consumer.start()
        logger.info(f"ShopConsumer started consume topic {self.topic}")
        try:
            async for message in self.consumer:
                with get_tracer(__name__).start_as_current_span("consume_shop_message") as span:
                    try:
                        user_data = ActionChestOpenDTO.model_validate_json(message.value)
                        await self.handle_action_chest_open(user_data)
                        await self.consumer.commit()
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                        logger.error(f"Validation error: {e}")

        finally:
            await self.consumer.stop()
            logger.info("ShopConsumer stopped")

    async def handle_action_chest_open(self, user_data: ActionChestOpenDTO):
        async with async_session() as session:
            try:
                await update_user(session, user_id=user_data.user_id, containers=1, experience=user_data.exp)
            except ValueError:
                pass