from typing import Iterator
import inject
from .models import Topic, TopicPartitions
from .ports import TopicInformationPort


class TopicService:

    __topic_information_port = inject.attr(TopicInformationPort)

    async def get_topics_information(self) -> Iterator[Topic]:
        topics = await self.__topic_information_port.get_topics()
        return (
            topic for topic in topics
            if not topic.name.startswith('_')
        )

    async def get_topic_offsets(self, topic_name) -> TopicPartitions:
        topic_informations = (
            await self.__topic_information_port
                      .get_topic_offsets(topic_name)
        )
        return topic_informations
