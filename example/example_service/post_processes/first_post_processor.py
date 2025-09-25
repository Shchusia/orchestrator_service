"""
Module first post process handler
"""

from typing import Any, Optional

from orch_serv import (
    AsyncCommandHandlerPostProcessStrategy,
    BaseOrchServMsg,
    CommandHandlerPostProcessStrategy,
)


class FirstPostProcessHandler(CommandHandlerPostProcessStrategy):
    def post_process(self, msg: BaseOrchServMsg, additional_data: Any | None = None):
        # do something
        pass


class FirstAsyncPostProcessHandler(AsyncCommandHandlerPostProcessStrategy):
    async def post_process(
        self, msg: BaseOrchServMsg, additional_data: Any | None = None
    ):
        # do something
        pass
