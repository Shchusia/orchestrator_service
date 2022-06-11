"""
Module second post process handler
"""

from typing import Any, Optional

from orch_serv import (
    AsyncCommandHandlerPostProcessStrategy,
    BaseOrchServMsg,
    CommandHandlerPostProcessStrategy,
)


class SecondPostProcessHandler(CommandHandlerPostProcessStrategy):
    def post_process(self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None):
        # do something
        pass


class SecondAsyncPostProcessHandler(AsyncCommandHandlerPostProcessStrategy):
    async def post_process(
        self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None
    ):
        # do something
        pass
