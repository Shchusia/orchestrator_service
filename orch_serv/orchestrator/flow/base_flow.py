"""
Module with classes for build flow
"""
# pylint: disable=no-else-return,too-few-public-methods
from __future__ import annotations

import types
from logging import Logger
from typing import Callable, Optional, Type, Union

from orch_serv.exc import (
    FlowBlockException,
    FlowBuilderException,
    WorkTypeMismatchException,
)
from orch_serv.orchestrator.block import AsyncBlock, SyncBlock


class FlowBlock:
    """
    Block for FlowBuilder
    """

    obj_block: Union[SyncBlock, AsyncBlock, type] = None

    def __init__(
        self,
        obj_block: Union[SyncBlock, AsyncBlock, type],
        pre_handler_function: Union[
            str, types.FunctionType, types.MethodType, Callable
        ] = None,
        post_handler_function: Union[
            str, types.FunctionType, types.MethodType, Callable
        ] = None,
    ):
        """
        Init FlowBlock
        :param obj_block: type stepBlock
        :param pre_handler_function
        :param  post_handler_function
        """
        try:
            if isinstance(obj_block, type):
                if getattr(obj_block, "__base__"):
                    if obj_block.__base__.__name__ in ["Block", "AsyncBlock"]:
                        self.obj_block = obj_block
                        self.pre_handler_function = pre_handler_function
                        self.post_handler_function = post_handler_function
                        return
                    elif issubclass(obj_block.__base__, (SyncBlock, AsyncBlock)):

                        self.obj_block = obj_block
                        self.pre_handler_function = pre_handler_function
                        self.post_handler_function = post_handler_function
                        return

            elif issubclass(type(obj_block), (SyncBlock, AsyncBlock)):
                self.obj_block = obj_block

                self.pre_handler_function = pre_handler_function
                self.post_handler_function = post_handler_function
                return

            raise FlowBlockException(str(type(obj_block)))
        except FlowBlockException as exc:
            raise exc
        except Exception:  # noqa
            raise TypeError("Incorrect type `obj_block`") from Exception

    @staticmethod
    def _get_function(
        instance_main: Flow,
        function_to_get: Union[str, types.FunctionType, types.MethodType, Callable],
    ) -> Optional[Union[types.FunctionType, types.MethodType, Callable]]:
        if isinstance(function_to_get, str):
            return getattr(instance_main, function_to_get, None)
        else:
            return function_to_get

    def init_block(
        self, instance_main: Flow, step_number: int = 0
    ) -> Union[SyncBlock, AsyncBlock]:
        """
        Method init instance subclass MainBlock
        :param instance_main:
        :param step_number:
        :return: object subclass MainBlock
        """
        if not isinstance(instance_main, Flow):
            raise TypeError("Value `instance_main` must be a Flow")
        result: Union[AsyncBlock, SyncBlock]
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
    build chain flow from flow blocks
    """

    def __init__(self, step: FlowBlock, *args):
        """
        Init FlowBuilder
        :param FlowBlock step: first block in flow
        :param List[FlowBlock] args:  other steps  if value exsst
        """
        self.steps = list(args)
        self.steps.insert(0, step)
        for _index, _step in enumerate(self.steps):
            if not isinstance(_step, FlowBlock):
                raise FlowBuilderException(f"on index {_index}")

    def build_flow(self, instance_main: Flow) -> SyncBlock:
        """
        Build chain flow for StrategyFlow
        :param instance_main:
        :return:
        """

        flow = self.steps[0].init_block(instance_main, 0)
        cur_step = flow
        for i, step in enumerate(self.steps[1:]):
            cur_step = cur_step.set_next(step.init_block(instance_main, i + 1))
        return flow


class Flow:
    """
    Class for inheritance for a specific flow
    """

    flow_chain: Union[SyncBlock, AsyncBlock] = None
    is_contains_duplicat_blocks: bool = False

    @property
    def name_flow(self) -> str:
        """
        Unique name to identify flow
        for override in subclass   name_flow
        :return: name flow
        """
        raise NotImplementedError

    @property
    def _base_class_for_blocks(self) -> Type:
        raise NotImplementedError

    @property
    def steps_flow(self):
        """
        Steps current flow
        :return:
        """
        raise NotImplementedError

    @steps_flow.setter
    def steps_flow(self, flow: FlowBuilder):
        """
        check the set value to property `steps_flow` value
        :param FlowBuilder flow: builder flow for current flow
        :return: None or exception
        """
        if isinstance(flow, FlowBuilder):
            self.steps_flow = flow
        else:
            raise TypeError("incorrect type flow builder")

    def __init__(self, logger: Optional[Logger] = None):
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

    def _validate_data(self):
        current = self.flow_chain
        while current:
            if not isinstance(current, self._base_class_for_blocks):
                raise WorkTypeMismatchException(
                    base_class=self.__class__.__name__,
                    obj_class=current.__class__.__name__,
                    is_target=False,
                )
            current = current.get_next()

    def get_steps(self) -> str:
        """
        Print steps flow
        :return:
        """
        return self.flow_chain.get_list_flow()
