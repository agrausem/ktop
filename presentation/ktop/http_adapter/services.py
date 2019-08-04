from aiohttp import web
import inject
from ktop.core.services import TopicService
from .adapters import (
    TopicPresentationAdapter,
    TopicPartitionsPresentationAdapter
)


class TopicsView(web.View):

    __topic_service: TopicService = inject.attr(TopicService)

    async def get(self):
        topics = await self.__topic_service.get_topics_information()
        topics = [
            TopicPresentationAdapter(topic).default()
            for topic in topics
        ]
        return web.json_response(topics)


class TopicView(web.View):

    __topic_service: TopicService = inject.attr(TopicService)

    async def get(self):
        topic = self.request.match_info['name']
        topic_offsets = await self.__topic_service.get_topic_offsets(topic)
        return web.json_response(
            TopicPartitionsPresentationAdapter(topic_offsets).default()
        )
