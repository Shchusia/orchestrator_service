"""
Sync Block
"""
# pylint: disable=not-callable
from __future__ import annotations

import types
from abc import ABC
from copy import deepcopy
from logging import Logger
from typing import Callable, Optional, Type, Union

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
    def is_execute_after_nullable_process_msg(self) -> bool:
        """
        Execute if the block handler did not return a message
        :return: true if should execute with previous msg after empty process msg
        :rtype: bool
        """
        return True

    @property
    def pre_handler_function(
        self,
    ) -> Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]:
        """
        A class property that returns an asynchronous function that will be
         called before being sent to the main handler.
        the function should only take one parameter msg: BaseOrchServMsg
        Attention!!!
        The function must return a message object.
        If the function does not return a message, then the handler will not be called
        :return: async function if exist pre_handler_function
        :rtype: Optional[Callable[[BaseOrchServMsg],
         Awaitable[Optional[BaseOrchServMsg]]]]
        """
        return self._pre_handler_function

    @property
    def post_handler_function(
        self,
    ) -> Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]:
        """
        A class property that returns an asynchronous function that will be
         called after this block`s handler.
        the function should only take one parameter msg: BaseOrchServMsg
        if the `process` does not return a message to the function,
         the message sent to the handler will be transferred
        if it is not necessary to execute, redefine
         the variable `is_execute_after_nullable_process_msg = False` in your block
        :return: async function if exist pre_handler_function
        :rtype: Optional[Callable[[BaseOrchServMsg],
         Awaitable[Optional[BaseOrchServMsg]]]]
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
        logger: Optional[Logger] = None,
    ):
        """
        Init Block
        :param pre_handler_function: function should accept
         and return objects of type Message
        which be run before call method
        :param post_handler_function: function should accept
         and return objects of type Message
        which be run after got msg from source
        :param logger: orchestrator logger
        """
        self.logger = logger or Logger(__name__)
        self.pre_handler_function = pre_handler_function  # type: ignore # noqa
        self.post_handler_function = post_handler_function  # type: ignore # noqa

    def set_next(
        self, handler: Union[SyncBaseBlock, Type[SyncBaseBlock]]
    ) -> SyncBaseBlock:
        """
        Save Next handler after this handler in flow
        :param handler: block for execution after current
        :type handler: Union[SyncBaseBlock, Type[SyncBaseBlock]]
        :return: SyncBaseBlock
        :raise Exception: some exception if error in time init handler if
         handler provided as type
        :raise TypeError: if handler not is instance of type SyncBaseBlock
        """
        if isinstance(handler, type):
            try:
                handler = handler()
            except Exception as exc:
                raise exc
        if not isinstance(handler, SyncBaseBlock):
            raise TypeError("Incorrect type for next handler")

        self._next_handler = handler
        return handler

    def get_next(self) -> Optional[SyncBaseBlock]:
        """
        the method returns the next block after the current one
        :return: next block if exist
        :rtype: Optional[SyncBaseBlock]
        """
        return self._next_handler

    def _process_logic(self, block: SyncBaseBlock, message: BaseOrchServMsg) -> None:
        """
        Auxiliary function in which the logic of working with additional
         functions is hidden
        :param block: block for processing
        :type block: SyncBaseBlock
        :param message: message for processing
        :type message: BaseOrchServMsg
        :return: nothing
        """
        if block.pre_handler_function:
            message = block.pre_handler_function(message)
        if not message:
            return
        message.set_source(block.name_block)
        copy_msg = deepcopy(message)
        new_msg = block.process(message)
        if block.post_handler_function:
            if new_msg:
                block.post_handler_function(new_msg)
            elif self.is_execute_after_nullable_process_msg:
                block.post_handler_function(copy_msg)

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
        if not message.get_source():
            self._process_logic(block=self, message=message)
        elif message.get_source() == self.name_block:
            self._process_logic(block=self._next_handler, message=message)
        elif self._next_handler:
            self._next_handler.handle(message)
        else:
            raise FlowException(f"Not found block for source: {message}")

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
