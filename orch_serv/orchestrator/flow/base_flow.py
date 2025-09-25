"""
Module with classes for build flow
"""

# pylint: disable=no-else-return,too-few-public-methods
from __future__ import annotations

from collections.abc import Callable
from logging import Logger, getLogger
import types
from typing import Any, Union

from orch_serv.exc import (
    FlowBlockException,
    FlowBuilderException,
    NotUniqueBlockInFlowError,
    WorkTypeMismatchException,
)
from orch_serv.orchestrator.block import AsyncBlock, SyncBlock
from orch_serv.orchestrator.block.base_block import AsyncBaseBlock, SyncBaseBlock


class FlowBlock:
    """
    Block for FlowBuilder
    """

    obj_block: SyncBlock | AsyncBlock | type = None  # type: ignore

    def __init__(
        self,
        obj_block: SyncBlock | AsyncBlock | type[SyncBlock | AsyncBlock],
        pre_handler_function: (
            str | types.FunctionType | types.MethodType | Callable | None
        ) = None,
        post_handler_function: (
            str | types.FunctionType | types.MethodType | Callable | None
        ) = None,
    ):
        """
        Init FlowBlock
        :param obj_block: block for flow
        :type obj_block: Union[SyncBlock, AsyncBlock,
         Type[Union[SyncBlock, AsyncBlock]]]
        :param pre_handler_function: optional function for execution before block
        :param  post_handler_function: optional function for execution after block
        """
        try:
            if isinstance(obj_block, type) and issubclass(
                obj_block, (SyncBlock, AsyncBlock)
            ):
                self.obj_block = obj_block
                self.pre_handler_function = pre_handler_function
                self.post_handler_function = post_handler_function
                return

            elif isinstance(obj_block, (SyncBlock, AsyncBlock)):
                self.obj_block = obj_block
                self.pre_handler_function = pre_handler_function
                self.post_handler_function = post_handler_function
                return

            raise FlowBlockException(str(type(obj_block)))
        except FlowBlockException as exc:
            raise exc

    @staticmethod
    def _get_function(
        instance_main: Flow,
        function_to_get: str | types.FunctionType | types.MethodType | Callable | None,
    ) -> types.FunctionType | types.MethodType | Callable | None:
        """
        helper function that returns a function if specified for the block
        :param instance_main:
        :type instance_main: Flow
        :param function_to_get: name of function or the function itself
        :type function_to_get: Union[str, types.FunctionType,
         types.MethodType, Callable]
        :return: a function object if provided
        :rtype: Optional[Union[types.FunctionType, types.MethodType, Callable]]
        """
        if isinstance(function_to_get, str):
            return getattr(instance_main, function_to_get, None)
        else:
            return function_to_get

    def init_block(
        self, instance_main: Flow, step_number: int = 0
    ) -> SyncBlock | AsyncBlock:
        """
        Method init instance subclass MainBlock
        :param instance_main: flow object for which this
         block is initialized
        :type instance_main: Flow
        :param int step_number: sequence number of the current block
        :return: object subclass MainBlock
        :rtype: Union[SyncBlock, AsyncBlock]
        """
        if not isinstance(instance_main, Flow):
            raise TypeError("Value `instance_main` must be a Flow")
        result: AsyncBlock | SyncBlock
        if isinstance(self.obj_block, type):

            result = self.obj_block(
                pre_handler_function=self._get_function(
                    instance_main, self.pre_handler_function
                ),
                post_handler_function=self._get_function(
                    instance_main, self.post_handler_function
                ),
                logger=instance_main.logger,
            )
            self.obj_block = result
        else:
            self.obj_block.pre_handler_function = self._get_function(  # type: ignore
                instance_main, self.pre_handler_function
            )
            self.obj_block.post_handler_function = self._get_function(  # type: ignore
                instance_main, self.post_handler_function
            )
            self.obj_block.logger = instance_main.logger
            result = self.obj_block
        if instance_main.is_contains_duplicat_blocks:
            result.name_block = result.name_block + f"_{step_number}"  # type: ignore
        return result


class FlowBuilder:
    """
    Flow building class
    build chain flow from its blocks
    """

    def __init__(self, step: FlowBlock, *args: Any) -> None:
        """
        Init FlowBuilder
        :param FlowBlock step: first block in flow
        :param List[FlowBlock] args:  other steps  if value exist
        """
        self.steps = list(args)
        self.steps.insert(0, step)
        for _index, _step in enumerate(self.steps):
            if not isinstance(_step, FlowBlock):
                raise FlowBuilderException(f"on index {_index}")

    def build_flow(self, instance_main: Flow) -> SyncBlock | AsyncBlock:
        """
        Build chain flow for Flow
        :param instance_main: current flow
        :type instance_main: Flow
        :return: the first block in the flow chain
        :rtype: Union[SyncBlock, AsyncBlock]
        """

        flow = self.steps[0].init_block(instance_main, 0)
        cur_step = flow
        for i, step in enumerate(self.steps[1:]):
            cur_step = cur_step.set_next(step.init_block(instance_main, i + 1))
        return flow


class Flow:
    """
    Class for inheritance for a specific flow
    :attr flow_chain: flow chain starting from the first block
    :type flow_chain: Union[SyncBlock, AsyncBlock]
    :attr is_contains_duplicat_blocks: whether the flow contains repeating blocks
     needed to avoid looping
    :type is_contains_duplicat_blocks: bool

    """

    flow_chain: SyncBaseBlock | AsyncBaseBlock | None = None
    is_contains_duplicat_blocks: bool = False

    @property
    def name_flow(self) -> str:
        """
        Unique name to identify flow
        for override in subclass 'name_flow'
        :return: name flow
        """
        raise NotImplementedError

    @property
    def _base_class_for_blocks(
        self,
    ) -> type[AsyncBlock | SyncBlock]:
        """
        An additional property for child classes to make the flow work only
         with synchronous or asynchronous blocks.
         necessary to maintain integrity
        :return:
        """
        raise NotImplementedError

    @property
    def steps_flow(self) -> FlowBuilder:
        """
        blocks that make up the current flow
        :return:
        """
        raise NotImplementedError

    # @steps_flow.setter
    # def steps_flow(self, flow: FlowBuilder):
    #     """
    #     check the set value to property `steps_flow` value
    #     :param FlowBuilder flow: builder flow for current flow
    #     :return: None or exception
    #     """
    #     getLogger(__name__).warning('iiiiiii')
    #     if isinstance(flow, FlowBuilder):
    #         self.flow_chain = flow.build_flow(self)
    #     else:
    #         raise TypeError("incorrect type flow builder")

    def __init__(self, logger: Logger | None = None):
        """
        Init Flow
        :param logger: orchestrator logger
        """
        self.logger = logger or Logger(__name__)
        self.logger.info("Init block %s", self.name_flow)

        if isinstance(self.steps_flow, FlowBuilder):
            self.flow_chain = self.steps_flow.build_flow(self)
        else:
            raise TypeError(
                f"Incorrect type 'steps_flow' - it must be 'FlowBuilder',"
                f" and not {type(self.steps_flow)}"
            )
        self._validate_data()

    def _validate_data(self) -> None:
        """
        flow validation function after initialization
        """
        current = self.flow_chain
        list_exists_blocks = list()
        while current:
            if not isinstance(current, self._base_class_for_blocks):
                raise WorkTypeMismatchException(
                    base_class=self.__class__.__name__,
                    obj_class=current.__class__.__name__,
                    is_target=False,
                )
            if current.name_block in list_exists_blocks:
                raise NotUniqueBlockInFlowError(
                    block_name=current.name_block, flow_name=self.name_flow
                )
            list_exists_blocks.append(current.name_block)
            current = current.get_next()

    def get_steps(self) -> str:
        """
        Print steps flow
        :return:
        """
        return self.flow_chain.get_list_flow()  # type: ignore
