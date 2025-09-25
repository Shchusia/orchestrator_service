"""
Flow for sync mode
"""

from abc import ABC

from orch_serv.msg import BaseOrchServMsg

from .. import SyncBlock
from ..block.base_block import SyncBaseBlock
from .base_flow import Flow


class SyncFlow(Flow, ABC):
    """
    SyncFlow for execution SyncBlock
    """

    _base_class_for_blocks: type = SyncBlock
    flow_chain: SyncBlock

    def to_go_with_the_flow(self, message: BaseOrchServMsg) -> None:
        """
        Method that starts flow execution from the first block
        :param message: message to process
        :type message: BaseOrchServMsg
        :return: None
        """
        self.flow_chain.handle(message)
