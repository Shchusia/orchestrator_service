"""
Flow for sync mode
"""
from abc import ABC
from typing import Union

from orch_serv.msg import BaseOrchServMsg

from .. import AsyncBlock
from .base_flow import Flow


class AsyncFlow(Flow, ABC):
    """
    AsyncFlow for execution async blocks
    """

    flow_chain: Union[AsyncBlock] = None

    async def to_go_with_the_flow(self, message: BaseOrchServMsg) -> None:
        """
        Method that starts flow execution from the first block
        :param message: message to process
        :type message: BaseOrchServMsg
        :return: None
        """
        await self.flow_chain.handle(message)
