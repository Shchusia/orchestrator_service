"""
Sync Block
"""
# pylint: disable=not-callable
import types
from abc import ABC
from typing import Callable, Optional

from orch_serv.exc import FlowException
from orch_serv.msg import BaseOrchServMsg

from .base_block import SyncBaseBlock


class SyncBlock(SyncBaseBlock, ABC):
    """
    The main class for inheriting the blocks that make up the flow of tasks execution
    """

    _next_handler: SyncBaseBlock = None
    _pre_handler_function: Optional[
        Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]
    ] = None
    _post_handler_function: Optional[
        Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]
    ] = None

    @property
    def pre_handler_function(
        self,
    ) -> Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]:
        """
        function which call before send to handler
        :return:
        """
        return self._pre_handler_function

    @property
    def post_handler_function(
        self,
    ) -> Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]:
        """
        function which call after received from source
        :return:
        """
        return self._post_handler_function

    @pre_handler_function.setter  # type: ignore
    def pre_handler_function(
        self,
        func: Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]] = None,
    ):
        """
        Method check pre_handler_function is func
        :param func: object to check
        :type func: Callable
        :raise TypeError: if func is not method or function
        :return: nothing
        """
        if not func:
            pass
        elif isinstance(func, (types.FunctionType, types.MethodType)):
            self._pre_handler_function = func
        else:
            raise TypeError(
                "Incorrect type pre_handler_function,"
                " the attribute must be a function or None"
            )

    @post_handler_function.setter  # type: ignore # noqa
    def post_handler_function(
        self,
        func: Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]] = None,
    ):
        """
        Method check post_handler_function is func
        :param func: object to check
        :type func: Callable
        :raise TypeError: if func is not method or function
        :return: nothing
        """
        if not func:
            pass
        elif isinstance(func, (types.FunctionType, types.MethodType)):
            self._post_handler_function = func
        else:
            raise TypeError(
                "Incorrect type post_handler_function,"
                " the attribute must be a function or None"
            )

    def __init__(
        self,
        pre_handler_function: Optional[
            Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]
        ] = None,
        post_handler_function: Optional[
            Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]
        ] = None,
    ):
        """
        Init Block
        :param pre_handler_function: function should accept
         and return objects of type Message
        which be run before call method
        :param post_handler_function: function should accept
         and return objects of type Message
        which be run after got msg from source

        """
        self.pre_handler_function = pre_handler_function  # type: ignore # noqa
        self.post_handler_function = post_handler_function  # type: ignore # noqa

    def set_next(self, handler: SyncBaseBlock) -> SyncBaseBlock:
        """
        Save Next handler after this handler
        :param handler:
        :return: Optional[BlockHandler, None]
        """
        self._next_handler = handler
        return handler

    def get_list_flow(self) -> str:
        """
        Method return str flow
        :return: str
        """
        if self._next_handler:
            next_blocks = self._next_handler.get_list_flow()
        else:
            next_blocks = "end"
        return f"{self.name_block} -> {next_blocks}"

    def handle(self, message: BaseOrchServMsg) -> None:
        """
        Method handle process msg
        :param BaseOrchServMsg message: msg to process
        :raise FlowException: if not found handle for source from message
        :return: nothing
        """
        if not message.get_source():
            # if message don't have `source`
            # we start from first chain flow
            message.set_source(self.name_block)
            self.process(message)
        elif message.get_source() == self.name_block:
            if self.post_handler_function:
                message = self.post_handler_function(message)
            if not message or not self._next_handler:
                # if after post handling don't return msg
                # or not next handler
                return
            if self._next_handler.pre_handler_function:
                message = self._next_handler.pre_handler_function(message)

            if not message:
                # if don't return message after processing
                return
            message.set_source(self._next_handler.name_block)
            self._next_handler.process(message)
        elif self._next_handler:
            self._next_handler.handle(message)
        else:
            raise FlowException(f"Not found block for source: {message}")
