from aiokafka import AIOKafkaProducer

from broker.config.preferences import KAFKA_SERVER
from broker.schemas.match.guild_war_respone import GuildWarResponseDTO


producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)

async def start_producer():
    await producer.start()

async def stop_producer():
    await producer.stop()

async def send_guild_war_end_message(topic: str, data: GuildWarResponseDTO):
    message = data.model_dump_json().encode("utf-8")
    await producer.send_and_wait(topic, message)
