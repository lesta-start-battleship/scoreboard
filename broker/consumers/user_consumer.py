from aiokafka import AIOKafkaConsumer
from pydantic_core._pydantic_core import ValidationError

from broker.schemas.user.new_user import NewUserDTO
from shared.database.database import async_session
from shared.repositories.user_repository import UserRepository


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
                try:
                    user_data = NewUserDTO.model_validate_json(message.value)
                except ValidationError as e:
                    print(f"Ошибка валидации данных: {e}")
                    continue

                async with async_session() as session:
                    user_repository = UserRepository(session=session)
                    await user_repository.create_user(user_data)

                await self.consumer.commit()
        finally:
            await self.consumer.stop()
