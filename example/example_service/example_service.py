from post_processes import (
    FirstAsyncPostProcessHandler,
    FirstPostProcessHandler,
    SecondAsyncPostProcessHandler,
    SecondPostProcessHandler,
)
from processes import FirstAsyncHandler, FirstHandler, SecondAsyncHandler, SecondHandler

from orch_serv import AsyncService, Service, ServiceBlock, ServiceBuilder


class ExampleService(Service):
    service_commands = ServiceBuilder(
        ServiceBlock(processor=FirstHandler, post_processor=FirstPostProcessHandler),
        ServiceBlock(processor=SecondHandler),
        default_post_process=SecondPostProcessHandler,
    )


class ExampleAsyncService(AsyncService):
    service_commands = ServiceBuilder(
        ServiceBlock(
            processor=FirstAsyncHandler, post_processor=FirstAsyncPostProcessHandler
        ),
        ServiceBlock(processor=SecondAsyncHandler),
        default_post_process=SecondAsyncPostProcessHandler,
    )


service = ExampleService()
async_service = ExampleAsyncService()
