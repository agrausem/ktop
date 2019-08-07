from typing import Tuple, Iterator

from aiokafka import AIOKafkaConsumer, TopicPartition


class TopicConsumer(AIOKafkaConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_partitions(self, topic) -> Iterator[TopicPartition]:
        return (
            TopicPartition(topic, partition)
            for partition in self.partitions_for_topic(topic)
        )

    async def get_offsets(self, partitions) -> Tuple[TopicPartition, TopicPartition]:
        begin = await self.beginning_offsets(partitions)
        end = await self.end_offsets(partitions)
        return begin, end
