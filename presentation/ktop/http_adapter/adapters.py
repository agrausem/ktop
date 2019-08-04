from ktop.core.models import Topic, TopicPartitions, Offsets
from .json import json_property, JsonSerializable


@JsonSerializable
class TopicPresentationAdapter:

    def __init__(self, delegate: Topic):
        self.__delegate = delegate

    @json_property
    def name(self) -> str:
        return self.__delegate.name

    @json_property
    def nb_partitions(self) -> int:
        return self.__delegate.nb_partitions


@JsonSerializable
class TopicPartitionsPresentationAdapter:

    def __init__(self, delegate: TopicPartitions):
        self.__delegate = delegate

    @json_property
    def topic(self):
        return self.__delegate.topic

    @json_property
    def offsets(self):
        return [
            OffsetsPresentationAdapter(p)
            for p in self.__delegate.partitions
        ]

    @json_property
    def messages(self):
        return self.__delegate.total_offsets


@JsonSerializable
class OffsetsPresentationAdapter:

    def __init__(self, delegate: Offsets):
        self.__delegate = delegate

    @json_property
    def begin(self):
        return self.__delegate.begin

    @json_property
    def end(self):
        return self.__delegate.end
