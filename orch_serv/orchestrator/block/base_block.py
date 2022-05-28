"""
Module with block class from which flow chains are formed
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Optional

from orch_serv.msg import BaseOrchServMsg


class SyncBaseBlock(ABC):
    """
    Base class for handling sync blocks
    """

    @property
    def pre_handler_function(
        self,
    ) -> Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]:
        """
        property for override in subclass
        """
        raise NotImplementedError

    @property
    def post_handler_function(
        self,
    ) -> Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]:
        """
        property for override in subclass
        """
        raise NotImplementedError

    @property
    def name_block(self):
        """
        Unique name to identify block
        for override in subclass   name_block
        """
        raise NotImplementedError

    @abstractmethod
    def set_next(self, handler: SyncBaseBlock) -> SyncBaseBlock:
        """
        method for adding a new handler
        :param BaseBlock handler: object next handler in chain flow
        :return: BlockHandler
        """
        raise NotImplementedError

    @abstractmethod
    def get_list_flow(self) -> str:
        """
        Method return str steps flow
        :return: str
        """
        raise NotImplementedError

    @abstractmethod
    def handle(self, message: BaseOrchServMsg) -> None:
        """
        flow chain management method
        :param MessageQueue message:
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def process(self, message: BaseOrchServMsg) -> None:
        """
        Method for executing the logic of a given block
        in it, only send messages to other services
        :param message: message to process
        :return: nothing
        """
        raise NotImplementedError("Not Implemented method for processing messages")


class AsyncBaseBlock(ABC):
    """
    Base class for handling async blocks
    """

    @property
    def pre_handler_function(
        self,
    ) -> Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]]:
        """
        property for override in subclass
        """
        raise NotImplementedError

    @property
    def post_handler_function(
        self,
    ) -> Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]]:
        """
        property for override in subclass
        """
        raise NotImplementedError

    @property
    def name_block(self):
        """
        Unique name to identify block
        for override in subclass   name_block
        """
        raise NotImplementedError

    @abstractmethod
    def set_next(self, handler: AsyncBaseBlock) -> AsyncBaseBlock:
        """
        method for adding a new handler
        :param BaseBlock handler: object next handler in chain flow
        :return: BlockHandler
        """
        raise NotImplementedError

    @abstractmethod
    def get_list_flow(self) -> str:
        """
        Method return str steps flow
        :return: str
        """
        raise NotImplementedError

    @abstractmethod
    async def handle(self, message: BaseOrchServMsg) -> None:
        """
        flow chain management method
        :param MessageQueue message:
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    async def process(self, message: BaseOrchServMsg) -> None:
        """
        Method for executing the logic of a given block
        in it, only send messages to other services
        :param message: message to process
        :return: nothing
        """
        raise NotImplementedError("Not Implemented method for processing messages")