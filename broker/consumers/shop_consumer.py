from aiokafka import AIOKafkaConsumer
from pydantic_core._pydantic_core import ValidationError

from broker.schemas.shop.action_chest_open import ActionChestOpenDTO
from shared.database.database import async_session
from shared.repositories.shop_repository import ShopRepository


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
        try:

            async for message in self.consumer:
                try:

                    user_data = ActionChestOpenDTO.model_validate_json(message.value)
                    await self.handle_action_chest_open(user_data)

                    await self.consumer.commit()

                except ValidationError as e:
                    print(f"Ошибка валидации данных: {e}")

        finally:
            await self.consumer.stop()

    async def handle_action_chest_open(self, user_data: ActionChestOpenDTO):
        async with async_session() as session:
            shop_repository = ShopRepository(session=session)
            new_user_data = user_data.model_dump()
            await shop_repository.open_chest(**new_user_data)
