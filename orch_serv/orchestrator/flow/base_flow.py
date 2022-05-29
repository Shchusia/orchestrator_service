"""
Module with classes for build flow
"""
# pylint: disable=no-else-return,too-few-public-methods
from __future__ import annotations

from logging import Logger
from typing import Optional, Union

from orch_serv.exc import FlowBlockException, FlowBuilderException
from orch_serv.orchestrator.block import AsyncBlock, SyncBlock


class FlowBlock:
    """
    Block for FlowBuilder
    """

    obj_block: Union[SyncBlock, AsyncBlock, type] = None

    def __init__(
        self,
        obj_block: Union[SyncBlock, AsyncBlock, type],
        pre_handler_function: str = None,
        post_handler_function: str = None,
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
                        self.pre_handler_function = str(pre_handler_function)
                        self.post_handler_function = str(post_handler_function)
                        return
                    elif issubclass(obj_block.__base__, (SyncBlock, AsyncBlock)):

                        self.obj_block = obj_block
                        self.pre_handler_function = str(pre_handler_function)
                        self.post_handler_function = str(post_handler_function)
                        return

            elif issubclass(type(obj_block), (SyncBlock, AsyncBlock)):
                self.obj_block = obj_block

                self.pre_handler_function = str(pre_handler_function)
                self.post_handler_function = str(post_handler_function)
                return

            raise FlowBlockException(str(type(obj_block)))
        except FlowBlockException as exc:
            raise exc
        except Exception:  # noqa
            raise TypeError("Incorrect type `obj_block`") from Exception

    def init_block(self, instance_main: Flow) -> Union[SyncBlock, AsyncBlock]:
        """
        Method init instance subclass MainBlock
        :param instance_main:
        :return: object subclass MainBlock
        """
        if not isinstance(instance_main, Flow):
            raise TypeError("Value `instance_main` must be a Flow")
        result: Union[AsyncBlock, SyncBlock]
        if isinstance(self.obj_block, type):
            result = self.obj_block(
                pre_handler_function=getattr(
                    instance_main, self.pre_handler_function, None
                ),
                post_handler_function=getattr(
                    instance_main, self.post_handler_function, None
                ),
                logger=instance_main.logger,
            )
            self.obj_block = result
        else:
            self.obj_block.pre_handler_function = getattr(  # type: ignore
                instance_main, self.pre_handler_function, None
            )
            self.obj_block.post_handler_function = getattr(  # type: ignore
                instance_main, self.post_handler_function, None
            )
            self.obj_block.logger = instance_main.logger
            result = self.obj_block
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
        flow = self.steps[0].init_block(instance_main)
        cur_step = flow
        for step in self.steps[1:]:
            cur_step = cur_step.set_next(step.init_block(instance_main))
        return flow


class Flow:
    """
    Class for inheritance for a specific flow
    """

    flow_chain: Union[SyncBlock, AsyncBlock] = None

    @property
    def name_flow(self) -> str:
        """
        Unique name to identify flow
        for override in subclass   name_flow
        :return: name flow
        """
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
        if isinstance(self.steps_flow, FlowBuilder):
            self.flow_chain = self.steps_flow.build_flow(self)
        else:
            raise TypeError(
                f"Incorrect type 'steps_flow' - it must be 'FlowBuilder',"
                f" and not {type(self.steps_flow)}"
            )

    def get_steps(self) -> str:
        """
        Print steps flow
        :return:
        """
        return self.flow_chain.get_list_flow()
