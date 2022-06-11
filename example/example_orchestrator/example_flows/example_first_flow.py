from typing import Optional

from example.example_orchestrator.example_blocks import (
    FirstAsyncBlock,
    FirstBlock,
    SecondAsyncBlock,
    SecondBlock,
)
from orch_serv import BaseOrchServMsg
from orch_serv.orchestrator import AsyncFlow, FlowBlock, FlowBuilder, SyncFlow


def other_method(message: BaseOrchServMsg) -> Optional[BaseOrchServMsg]:
    # do something
    pass


async def other_async_method(message: BaseOrchServMsg) -> Optional[BaseOrchServMsg]:
    # do something
    pass


class FirstFlow(SyncFlow):
    name_flow = "first_flow"
    is_contains_duplicat_blocks = True
    steps_flow = FlowBuilder(
        FlowBlock(
            FirstBlock,
            pre_handler_function="static_flow_method",
            post_handler_function=other_method,
        ),
        FlowBlock(
            SecondBlock,
            pre_handler_function=other_method,
            post_handler_function="static_flow_method",
        ),
        FlowBlock(
            FirstBlock,
            pre_handler_function="static_flow_method",
            post_handler_function=other_method,
        ),
    )

    @staticmethod
    def static_flow_method(message: BaseOrchServMsg) -> Optional[BaseOrchServMsg]:
        # do something
        pass


class FirstAsyncFlow(AsyncFlow):
    name_flow = "first_async_flow"

    steps_flow = FlowBuilder(
        FlowBlock(
            FirstAsyncBlock,
            pre_handler_function="static_flow_async_method",
            post_handler_function=other_async_method,
        ),
        FlowBlock(
            SecondAsyncBlock,
            pre_handler_function=other_async_method,
            post_handler_function="static_flow_async_method",
        ),
    )

    @staticmethod
    async def static_flow_async_method(
        message: BaseOrchServMsg,
    ) -> Optional[BaseOrchServMsg]:
        # do something
        pass
