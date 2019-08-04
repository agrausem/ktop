from abc import ABCMeta, abstractmethod


class TopicInformationPort(metaclass=ABCMeta):

    @abstractmethod
    async def get_topics(self):
        pass

    @abstractmethod
    async def get_topic_offsets(topic_name):
        pass
