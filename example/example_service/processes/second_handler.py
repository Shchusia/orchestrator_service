"""
Module first handler
"""
from typing import Any, Tuple, Union

from orch_serv import (
    AsyncCommandHandlerProcessStrategy,
    BaseOrchServMsg,
    CommandHandlerProcessStrategy,
)


class SecondHandler(CommandHandlerProcessStrategy):
    """
    Sync handler
    """

    target_command = "second_command"

    def process(
        self, msg: BaseOrchServMsg
    ) -> Union[Tuple[BaseOrchServMsg, Any], BaseOrchServMsg]:
        # do something
        return msg


class SecondAsyncHandler(AsyncCommandHandlerProcessStrategy):
    """
    Async handler
    """

    target_command = "second_async_command"

    async def process(
        self, msg: BaseOrchServMsg
    ) -> Union[Tuple[BaseOrchServMsg, Any], BaseOrchServMsg]:
        # do something
        return msg
