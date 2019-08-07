import asyncio

from aiohttp import web
import inject

from ktop.http_adapter.services import TopicsView, TopicView
from ktop.kafka_adapter.consumer import TopicConsumer
from ktop.http_application.config import create_config


loop = asyncio.get_event_loop()


async def topic_client(app):
    app['topic_consumer'] = TopicConsumer(
        loop=loop,
        bootstrap_servers='localhost:9093'
    )
    await app['topic_consumer'].start()
    yield
    await app['topic_consumer'].stop()


async def dependencies(app):
    inject.configure(create_config(app))


app = web.Application()

app.cleanup_ctx.append(topic_client)
app.on_startup.append(dependencies)

app.add_routes([web.view('/topics', TopicsView)])
app.add_routes([web.view('/topics/{name}', TopicView)])
web.run_app(app)
