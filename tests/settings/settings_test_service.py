from typing import Any, Optional

from pydantic import BaseModel

from orch_serv.msg import BaseOrchServMsg
from orch_serv.service import (
    AsyncCommandHandlerPostProcessStrategy,
    AsyncCommandHandlerProcessStrategy,
    AsyncService,
    CommandHandlerPostProcessStrategy,
    CommandHandlerProcessStrategy,
    Service,
    ServiceBlock,
    ServiceBuilder,
)

CONST_LIST_SYNC = []
CONST_LIST_ASYNC = []


class BodyModel(BaseModel):
    base_option: Optional[str]
    with_error: Optional[bool]


class HeaderModel(BaseModel):
    command: Optional[str]


class ServiceTestMessage(BaseOrchServMsg):
    body: BodyModel
    header: HeaderModel

    def get_command(self) -> Optional[str]:
        return self.header.command


class FirstProcessHandler(CommandHandlerProcessStrategy):
    target_command = "FirstProcessHandler"

    def process(self, message: BaseOrchServMsg):
        CONST_LIST_SYNC.append(1)
        return message


class SecondProcessHandler(CommandHandlerProcessStrategy):
    target_command = "SecondProcessHandler"

    def process(self, message: BaseOrchServMsg):
        CONST_LIST_SYNC.append(2)
        return message


class ThirdProcessHandler(CommandHandlerProcessStrategy):
    target_command = "ThirdProcessHandler"

    def process(self, message: BaseOrchServMsg):
        CONST_LIST_SYNC.append(3)
        if message.body.with_error is True:
            raise ValueError
        return None


class FirstPostProcessHandler(CommandHandlerPostProcessStrategy):
    def post_process(
        self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None
    ) -> None:
        CONST_LIST_SYNC.append(4)
        pass


class SecondPostProcessHandler(CommandHandlerPostProcessStrategy):
    def post_process(
        self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None
    ) -> None:
        CONST_LIST_SYNC.append(5)
        pass


class ThirdPostProcessHandler(CommandHandlerPostProcessStrategy):
    def post_process(
        self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None
    ) -> None:
        CONST_LIST_SYNC.append(6)
        pass


class FirstAsyncProcessHandler(AsyncCommandHandlerProcessStrategy):
    target_command = "FirstAsyncProcessHandler"

    async def process(self, message: BaseOrchServMsg):
        CONST_LIST_ASYNC.append(1)
        return message


class SecondAsyncProcessHandler(AsyncCommandHandlerProcessStrategy):
    target_command = "SecondAsyncProcessHandler"

    async def process(self, message: BaseOrchServMsg):
        CONST_LIST_ASYNC.append(2)
        return message


class ThirdAsyncProcessHandler(AsyncCommandHandlerProcessStrategy):
    target_command = "ThirdAsyncProcessHandler"

    async def process(self, message: BaseOrchServMsg):
        CONST_LIST_ASYNC.append(3)

        if message.body.with_error is True:
            raise ValueError
        return None


class FirstAsyncPostProcessHandler(AsyncCommandHandlerPostProcessStrategy):
    async def post_process(
        self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None
    ) -> None:
        CONST_LIST_ASYNC.append(4)
        pass


class SecondAsyncPostProcessHandler(AsyncCommandHandlerPostProcessStrategy):
    async def post_process(
        self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None
    ) -> None:
        CONST_LIST_ASYNC.append(5)
        pass


class ThirdAsyncPostProcessHandler(AsyncCommandHandlerPostProcessStrategy):
    async def post_process(
        self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None
    ) -> None:
        CONST_LIST_ASYNC.append(5)
        pass


class MySyncService(Service):
    service_commands = ServiceBuilder(
        ServiceBlock(
            processor=FirstProcessHandler, post_processor=FirstPostProcessHandler
        ),
        ServiceBlock(
            processor=SecondProcessHandler,
        ),
        ServiceBlock(
            processor=ThirdProcessHandler, post_processor=ThirdPostProcessHandler
        ),
        default_post_process=SecondPostProcessHandler,
    )


class MyAsyncService(AsyncService):
    service_commands = ServiceBuilder(
        ServiceBlock(
            processor=FirstAsyncProcessHandler,
            post_processor=FirstAsyncPostProcessHandler,
        ),
        ServiceBlock(
            processor=SecondAsyncProcessHandler,
        ),
        ServiceBlock(
            processor=ThirdAsyncProcessHandler,
            post_processor=ThirdAsyncPostProcessHandler,
        ),
        default_post_process=SecondAsyncPostProcessHandler,
    )


msg_to_first_handler = ServiceTestMessage(
    body=dict(), header=dict(command=FirstProcessHandler.target_command)
)
msg_to_second_handler = ServiceTestMessage(
    body=dict(), header=dict(command=SecondProcessHandler.target_command)
)
msg_to_third_handler = ServiceTestMessage(
    body=dict(), header=dict(command=ThirdProcessHandler.target_command)
)
msg_to_forth_handler = ServiceTestMessage(
    body=dict(), header=dict(command="not existed")
)
msg_to_third_handler_with_error = ServiceTestMessage(
    body=dict(with_error=True), header=dict(command=ThirdProcessHandler.target_command)
)

msg_to_async_first_handler = ServiceTestMessage(
    body=dict(), header=dict(command=FirstAsyncProcessHandler.target_command)
)
msg_to_async_second_handler = ServiceTestMessage(
    body=dict(), header=dict(command=SecondAsyncProcessHandler.target_command)
)
msg_to_async_third_handler = ServiceTestMessage(
    body=dict(), header=dict(command=ThirdAsyncProcessHandler.target_command)
)
msg_to_async_forth_handler = ServiceTestMessage(
    body=dict(), header=dict(command="not existed")
)
msg_to_async_third_handler_with_error = ServiceTestMessage(
    body=dict(with_error=True),
    header=dict(command=ThirdAsyncProcessHandler.target_command),
)
