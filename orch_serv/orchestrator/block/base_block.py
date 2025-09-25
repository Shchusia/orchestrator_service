"""
Module with block class from which flow chains are formed
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Optional

from orch_serv.msg import BaseOrchServMsg


class SyncBaseBlock(ABC):
    """
    Base class for handling sync blocks
    """

    @property
    def pre_handler_function(
        self,
    ) -> Callable[[BaseOrchServMsg], BaseOrchServMsg | None] | None:
        """
        The function that will be executed before the main handler
         must return a message if the message is not returned,
         then the message will not get into the handler
        """
        raise NotImplementedError

    @property
    def post_handler_function(
        self,
    ) -> Callable[[BaseOrchServMsg], BaseOrchServMsg | None] | None:
        """
        function to be executed after the main handler
        """
        raise NotImplementedError

    @property
    def name_block(self) -> str:
        """
        Unique name to identify block
        for override in subclass   name_block
        """
        raise NotImplementedError

    @abstractmethod
    def set_next(self, handler: SyncBaseBlock) -> SyncBaseBlock:
        """
        Save Next handler after this handler in flow
        :param  handler: block for execution after current
        :type  handler: Union[AsyncBaseBlock, Type[AsyncBaseBlock]]
        :return: AsyncBaseBlock
        :raise Exception: some exception if error is in time init handler if
         handler provided as type
        :raise TypeError: if handler is not instance of type SyncBaseBlock
        """
        raise NotImplementedError

    @abstractmethod
    def get_next(self) -> SyncBaseBlock:
        """
        the method returns the next block after
        :return: next block if exist
        :rtype: Optional[AsyncBaseBlock]
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
        A function that determines which handler should now process
         the message based on the source from which the message came.
        :param message: message for processing
        :type message: BaseOrchServMsg
        :return: nothing
        :raise FlowException: exception if a message with the wrong source
         is passed to the flow
        """
        raise NotImplementedError

    @abstractmethod
    def process(self, message: BaseOrchServMsg) -> BaseOrchServMsg | None:
        """
        Function to be redefined in subclasses which contains
         the main logic of this block
        If necessary, after executing this function, execute
         the post function method that must return a message
        :param message: message to process
        :type message: BaseOrchServMsg
        :return: message after processing
        :rtype: Optional[BaseOrchServMsg]
        """
        raise NotImplementedError("Not Implemented method for processing messages")


class AsyncBaseBlock(ABC):
    """
    Base class for handling async blocks
    """

    @property
    def pre_handler_function(
        self,
    ) -> Callable[[BaseOrchServMsg], Awaitable[BaseOrchServMsg | None]] | None:
        """
        The function that will be executed before the main handler.
         Must return a message, if the message is not returned,
         then the message will not get into the handler
        """
        raise NotImplementedError

    @property
    def post_handler_function(
        self,
    ) -> Callable[[BaseOrchServMsg], Awaitable[BaseOrchServMsg | None]] | None:
        """
        function to be executed after the main handler
        """
        raise NotImplementedError

    @property
    def name_block(self) -> str:
        """
        Unique name to identify block
        to override in subclass name_block
        """
        raise NotImplementedError

    @abstractmethod
    def set_next(self, handler: AsyncBaseBlock) -> AsyncBaseBlock:
        """
        Save next handler after this handler in flow
        :param  handler: block for execution after current
        :type  handler: Union[AsyncBaseBlock, Type[AsyncBaseBlock]]
        :return: AsyncBaseBlock
        :raise Exception: some exception if error in time init handler if
         handler provided as type
        :raise TypeError: if handler not is instance of type SyncBaseBlock
        """
        raise NotImplementedError

    @abstractmethod
    def get_next(self) -> AsyncBaseBlock | None:
        """
        the method returns the next block after
        :return: next block if exist
        :rtype: Optional[AsyncBaseBlock]
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
        A function that determines which handler should now process
         the message based on the source from which the message came.
        :param message: message for processing
        :type message: BaseOrchServMsg
        :return: nothing
        :raise FlowException: exception if a message with the wrong source
         is passed to the flow
        """
        raise NotImplementedError

    @abstractmethod
    async def process(self, message: BaseOrchServMsg) -> BaseOrchServMsg | None:
        """
        Function to be redefined in subclasses which contains
         the main logic of this block
        If necessary, after executing this function, execute
         the post function method must return a message
        :param message: message to process
        :type message: BaseOrchServMsg
        :return: message after processing
        :rtype: Optional[BaseOrchServMsg]
        """
        raise NotImplementedError("Not Implemented method for processing messages")
