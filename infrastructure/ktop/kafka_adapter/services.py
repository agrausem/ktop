from typing import Tuple

from aiokafka import TopicPartition
import inject

from ktop.core.ports import TopicInformationPort
from .adapters import TopicPartitionsCoreAdapter, TopicCoreAdapter
from .consumer import TopicConsumer


class TopicInformationPortService(TopicInformationPort):

    __consumer: TopicConsumer = inject.attr(TopicConsumer)

    async def get_topics(self):
        topics = await self.__consumer.topics()
        topics_with_partitions = (
            (topic, self.count_partitions(topic))
            for topic in topics
        )
        return (
            TopicCoreAdapter(twp)
            for twp in topics_with_partitions
        )

    def count_partitions(self, topic_name):
        return len(
            self.__consumer.partitions_for_topic(topic_name)
        )

    async def get_topic_offsets(self, topic_name):
        partitions = list(self.__consumer.get_partitions(topic_name))
        begin, end = await self.__consumer.get_offsets(partitions)

        def by_partition(offset: Tuple[TopicPartition, int]):
            return offset[0].partition

        partitions_with_offsets = zip(
            sorted(begin.items(), key=by_partition),
            sorted(end.items(), key=by_partition)
        )

        return TopicPartitionsCoreAdapter(partitions_with_offsets)
