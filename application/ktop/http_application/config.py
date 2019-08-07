from ktop.core.services import TopicService
from ktop.core.ports import TopicInformationPort
from ktop.kafka_adapter.consumer import TopicConsumer
from ktop.kafka_adapter.services import TopicInformationPortService


def create_config(app):

    consumer = app['topic_consumer']

    def config(binder):
        binder.bind(TopicConsumer, consumer)
        binder.bind_to_constructor(
            TopicInformationPort, TopicInformationPortService
        )
        binder.bind_to_constructor(TopicService, TopicService)

    return config
