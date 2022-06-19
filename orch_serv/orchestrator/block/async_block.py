"""
Module with base block class for user async blocks
"""
# pylint: disable=not-callable, inconsistent-mro
import types
from abc import ABC
from copy import deepcopy
from logging import Logger
from typing import Awaitable, Callable, Optional, Type, Union

from orch_serv.exc import FlowException
from orch_serv.msg import BaseOrchServMsg

from .base_block import AsyncBaseBlock


class AsyncBlock(AsyncBaseBlock, ABC):
    """
    Base block for async mode
    :attr _next_handler: the object of the next handler
     in the flow where this block participates
    :type _next_handler: AsyncBaseBlock
    :attr _pre_handler_function: function called before this block's handler
    :type _pre_handler_function:  Optional[
        Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]
    ]
    :attr _post_handler_function: function called after this block's handler
    :type _post_handler_function:  Optional[
        Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]
    ]
    """

    _next_handler: AsyncBaseBlock = None
    _pre_handler_function: Optional[
        Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]
    ] = None
    _post_handler_function: Optional[
        Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]
    ] = None

    @property
    def is_execute_after_nullable_process_msg(self) -> bool:
        """
        Execute if the block handler did not return a message
        :return: true if it should be executed with previous msg after empty process msg
        :rtype: bool
        """
        return True

    @property
    def pre_handler_function(
        self,
    ) -> Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]]:
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
    ) -> Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]]:
        """
        A class property that returns an asynchronous function that will be
         called after this block`s handler.
        the function should only take one parameter msg: BaseOrchServMsg
        if the `process` does not return a message to the function,
         the message sent to the handler will be transferred
        if it is not mandatory to execute, redefine
         the variable `is_execute_after_nullable_process_msg = False` in your block
        :return: async function if exist pre_handler_function
        :rtype: Optional[Callable[[BaseOrchServMsg],
         Awaitable[Optional[BaseOrchServMsg]]]]
        """
        return self._post_handler_function

    @pre_handler_function.setter  # type:ignore
    def pre_handler_function(
        self,
        func: Optional[
            Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]
        ] = None,
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
        elif isinstance(
            func, (types.FunctionType, types.MethodType, types.CoroutineType)
        ):
            self._pre_handler_function = func
        else:
            raise TypeError(
                "Incorrect type pre_handler_function,"
                " the attribute must be a function or None"
            )

    @post_handler_function.setter  # type:ignore
    def post_handler_function(
        self,
        func: Optional[
            Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]
        ] = None,
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
        elif isinstance(
            func, (types.FunctionType, types.MethodType, types.CoroutineType)
        ):
            self._post_handler_function = func
        else:
            raise TypeError(
                "Incorrect type post_handler_function,"
                " the attribute must be a function or None"
            )

    def __init__(
        self,
        pre_handler_function: Optional[
            Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]
        ] = None,
        post_handler_function: Optional[
            Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]
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
        self, handler: Union[AsyncBaseBlock, Type[AsyncBaseBlock]]
    ) -> AsyncBaseBlock:
        """
        Save next handler after this handler in flow
        :param  handler: block for execution after current
        :type  handler: Union[AsyncBaseBlock, Type[AsyncBaseBlock]]
        :return: AsyncBaseBlock
        :raise Exception: some exception if error in time init handler if
         handler provided as type
        :raise TypeError: if handler not is instance of type SyncBaseBlock
        """
        if isinstance(handler, type):
            try:
                handler = handler()
            except Exception as exc:
                raise exc
        if not isinstance(handler, AsyncBaseBlock):
            raise TypeError("Incorrect type for next handler")
        self._next_handler = handler
        return handler

    def get_next(self) -> Optional[AsyncBaseBlock]:
        """
        the method returns the next block
        :return: next block if exist
        :rtype: Optional[AsyncBaseBlock]
        """
        return self._next_handler

    async def _process_logic(
        self, block: AsyncBaseBlock, message: BaseOrchServMsg
    ) -> None:
        """
        Auxiliary function in which the logic of working with additional
         functions is hidden
        :param block: block for processing
        :type block: AsyncBaseBlock
        :param message: message for processing
        :type message: BaseOrchServMsg
        :return: nothing
        """
        if block.pre_handler_function:
            message = await block.pre_handler_function(message)
        if not message:
            return
        message.set_source(block.name_block)
        copy_msg = deepcopy(message)
        new_msg = await block.process(message)
        if block.post_handler_function:
            if new_msg:
                await block.post_handler_function(new_msg)
            elif self.is_execute_after_nullable_process_msg:
                await block.post_handler_function(copy_msg)

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
        if not message.get_source():
            await self._process_logic(block=self, message=message)
        elif message.get_source() == self.name_block:
            await self._process_logic(block=self._next_handler, message=message)
        elif self._next_handler:
            await self._next_handler.handle(message)
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
