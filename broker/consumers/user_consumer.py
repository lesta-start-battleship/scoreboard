from aiokafka import AIOKafkaConsumer
from pydantic_core._pydantic_core import ValidationError

from broker.config.preferences import NEW_USER_TOPIC, USERNAME_CHANGE_TOPIC, CURRENCY_CHANGE_TOPIC
from broker.schemas.user.currency_change import CurrencyChangeDTO
from broker.schemas.user.new_user import NewUserDTO
from broker.schemas.user.username_change import UsernameChangeDTO
from shared.database.database import async_session
from shared.repositories.user_repository import UserRepository


class UserConsumer:
    def __init__(self, kafka_servers: str, topic: str):
        self.topic = topic
        self.kafka_servers = kafka_servers
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.kafka_servers,
            group_id="user_group_consumer"
        )

    async def consume(self):
        await self.consumer.start()
        try:

            async for message in self.consumer:
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

                except ValidationError as e:
                    print(f"Ошибка валидации данных: {e}")

        finally:
            await self.consumer.stop()

    async def handle_new_user(self, user_data: NewUserDTO):
        async with async_session() as session:
            user_repository = UserRepository(session=session)
            new_user = user_data.model_dump()
            currency = new_user.pop("currencies", {})
            new_user_flat = {**new_user, **currency}
            await user_repository.create_user(**new_user_flat)

    async def handle_username_change(self, user_data: UsernameChangeDTO):
        async with async_session() as session:
            user_repository = UserRepository(session=session)
            new_user_data = user_data.model_dump()
            await user_repository.update_username(**new_user_data)

    async def handle_currency_change(self, user_data: CurrencyChangeDTO):
        async with async_session() as session:
            user_repository = UserRepository(session=session)
            new_user_data = user_data.model_dump()
            currency = new_user_data.pop("currencies", {})
            new_user_data_flat = {**new_user_data, **currency}
            await user_repository.create_user(**new_user_data_flat)
