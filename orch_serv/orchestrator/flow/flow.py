"""
Flow for sync mode
"""
from abc import ABC
from typing import Union

from orch_serv.msg import BaseOrchServMsg

from .. import SyncBlock
from .base_flow import Flow


class SyncFlow(Flow, ABC):
    """
    SyncFlow for execution SyncBlock
    """

    _base_class_for_blocks = SyncBlock
    flow_chain: Union[SyncBlock] = None

    def to_go_with_the_flow(self, message: BaseOrchServMsg) -> None:
        """
        Method that starts flow execution from the first block
        :param message: message to process
        :type message: BaseOrchServMsg
        :return: None
        """
        self.flow_chain.handle(message)
