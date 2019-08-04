from abc import ABCMeta, abstractproperty
from typing import List


class Topic(metaclass=ABCMeta):

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def nb_partitions(self) -> int:
        pass


class Offsets(metaclass=ABCMeta):

    @abstractproperty
    def begin(self) -> int:
        pass

    @abstractproperty
    def end(self) -> int:
        pass


class TopicPartitions(metaclass=ABCMeta):

    @abstractproperty
    def topic(self) -> str:
        pass

    @abstractproperty
    def partitions(self) -> List[Offsets]:
        pass

    @abstractproperty
    def total_offsets(self) -> int:
        pass
