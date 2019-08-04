from typing import Tuple, Iterator
from aiokafka import TopicPartition
from ktop.core.models import Topic, TopicPartitions, Offsets


class TopicCoreAdapter:

    def __init__(self, topic_with_partition: Tuple[str, int]):
        self.__topic_with_partition = topic_with_partition

    @property
    def name(self):
        return self.__topic_with_partition[0]

    @property
    def nb_partitions(self):
        return self.__topic_with_partition[1]


class TopicPartitionsCoreAdapter:

    def __init__(self, partitions: Iterator[Tuple[TopicPartition, TopicPartition]]):
        self.__partitions = list(partitions)

    @property
    def topic(self):
        return self.__partitions[0][0][0].topic

    @property
    def partitions(self):
        return [
            OffsetsCoreAdapter(offsets)
            for offsets in self.__partitions
        ]

    @property
    def total_offsets(self):
        return sum(
            [
                end[1] - begin[1] for begin, end in self.__partitions
            ]
        )


class OffsetsCoreAdapter:

    def __init__(self, offsets):
        self.__offsets = offsets

    @property
    def begin(self):
        return self.__offsets[0][1]

    @property
    def end(self):
        return self.__offsets[1][1]


Topic.register(TopicCoreAdapter)
TopicPartitions.register(TopicPartitionsCoreAdapter)
Offsets.register(OffsetsCoreAdapter)
