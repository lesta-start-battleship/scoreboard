from aiokafka import AIOKafkaProducer

from broker.schemas.match.guild_war_respone import GuildWarResponseDTO


class GuildWarProducer:
    def __init__(self, kafka_servers: str, topic: str):
        self.kafka_servers = kafka_servers
        self.topic = topic
        self.producer = AIOKafkaProducer(bootstrap_servers=self.kafka_servers)

    async def start_producer(self):
        await self.producer.start()

    async def stop_producer(self):
        await self.producer.start()

    async def send_guild_war_end_message(self, topic: str, data: GuildWarResponseDTO):
        message = data.model_dump_json().encode("utf-8")
        await self.producer.send_and_wait(topic, message)
