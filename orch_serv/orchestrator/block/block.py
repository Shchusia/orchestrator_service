"""
Module with block class from which flow chains are formed
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from orch_serv import BaseOrchServMsg


class BaseBlock(ABC):
    """
    The Handler interface declares a method for building a chain of handlers.
    It also declares a method to fulfill the request.
    """

    pre_handler_function = None
    post_handler_function = None

    @abstractmethod
    def set_next(self, handler: BaseBlock) -> BaseBlock:
        """
        method for adding a new handler
        :param BaseBlock handler: object next handler in chain flow
        :return: BlockHandler
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
    def get_list_flow(self) -> str:
        """
        Method return str steps flow
        :return: str
        """
        raise NotImplementedError
