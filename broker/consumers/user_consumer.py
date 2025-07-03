from aiokafka import AIOKafkaConsumer
from pydantic_core._pydantic_core import ValidationError

from app.schemas.user import UserSchema


class UserConsumer:
    def __init__(self, kafka_servers: str, topic: str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=kafka_servers,
            group_id="user_group_consumer"
        )

    async def consume(self):
        await self.consumer.start()
        try:
            async for message in self.consumer:
                user_data = UserSchema.model_validate_json(message.value)
                # TODO добавить добавление user_data в БД
        except ValidationError as e:
            print(f"Ошибка валидации данных: {e}")
        finally:
            await self.consumer.stop()
