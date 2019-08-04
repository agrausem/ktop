from aiohttp import web
from ktop.core.services import TopicService
from ktop.core.ports import TopicInformationPort
from ktop.http_adapter.services import TopicsView, TopicView
from ktop.kafka_adapter.consumer import (
    start_polling_topics,
    TopicConsumer,
    get_consumer
)
from ktop.kafka_adapter.services import TopicInformationPortService
import asyncio
import inject

loop = asyncio.get_event_loop()


def config(binder):
    consumer = get_consumer(loop)
    binder.bind(TopicConsumer, consumer)
    binder.bind_to_constructor(
        TopicInformationPort, TopicInformationPortService
    )
    binder.bind_to_constructor(TopicService, TopicService)


inject.configure(config)

loop.create_task(start_polling_topics())

app = web.Application()
app.add_routes([web.view('/topics', TopicsView)])
app.add_routes([web.view('/topics/{name}', TopicView)])
web.run_app(app)
