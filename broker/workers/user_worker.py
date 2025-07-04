import asyncio

from broker.config.preferences import USER_SERVER, NEW_USER_TOPIC, USERNAME_CHANGE_TOPIC, CURRENCY_CHANGE_TOPIC
from broker.consumers.user_consumer import UserConsumer


async def main():
    consumer_new_user = UserConsumer(USER_SERVER, NEW_USER_TOPIC)
    consumer_username_change = UserConsumer(USER_SERVER, USERNAME_CHANGE_TOPIC)
    consumer_currency_change = UserConsumer(USER_SERVER, CURRENCY_CHANGE_TOPIC)

    task1 = asyncio.create_task(consumer_new_user.consume())
    task2 = asyncio.create_task(consumer_username_change.consume())
    task3 = asyncio.create_task(consumer_currency_change.consume())

    await asyncio.gather(task1, task2, task3)


if __name__ == '__main__':
    asyncio.run(main())
