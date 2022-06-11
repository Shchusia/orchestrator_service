"""
Module first handler
"""
from typing import Any, Tuple, Union

from orch_serv import (
    AsyncCommandHandlerProcessStrategy,
    BaseOrchServMsg,
    CommandHandlerProcessStrategy,
)


class FirstHandler(CommandHandlerProcessStrategy):
    """
    Sync handler
    """

    target_command = "first_command"

    def process(
        self, msg: BaseOrchServMsg
    ) -> Union[Tuple[BaseOrchServMsg, Any], BaseOrchServMsg]:
        # do something
        return msg


class FirstAsyncHandler(AsyncCommandHandlerProcessStrategy):
    """
    Async handler
    """

    target_command = "first_async_command"

    async def process(
        self, msg: BaseOrchServMsg
    ) -> Union[Tuple[BaseOrchServMsg, Any], BaseOrchServMsg]:
        # do something
        return msg
