from orch_serv import AsyncFlow, BaseOrchServMsg, FlowBlock, FlowBuilder, SyncFlow

from .settings_test_block import (
    CONST_LIST_ASYNC,
    CONST_LIST_SYNC,
    FirstAsyncBlock,
    FirstBlock,
    SecondAsyncBlock,
    SecondBlock,
    async_tst_method_with_correct_processing,
    tst_method_with_correct_processing,
)


class TestFlow(SyncFlow):
    name_flow = "test_flow"

    steps_flow = FlowBuilder(
        FlowBlock(
            FirstBlock,
            pre_handler_function="tst_method_with_correct_processing",
            post_handler_function=tst_method_with_correct_processing,
        ),
        FlowBlock(
            SecondBlock,
            pre_handler_function=tst_method_with_correct_processing,
            post_handler_function="tst_method_with_correct_processing",
        ),
    )

    @staticmethod
    def tst_method_with_correct_processing(message: BaseOrchServMsg):
        CONST_LIST_SYNC.append(-3)
        return message


class TestAsyncFlow(AsyncFlow):
    name_flow = "test_async_flow"

    steps_flow = FlowBuilder(
        FlowBlock(
            FirstAsyncBlock,
            pre_handler_function="async_tst_method_with_correct_processing",
            post_handler_function=async_tst_method_with_correct_processing,
        ),
        FlowBlock(
            SecondAsyncBlock,
            pre_handler_function=async_tst_method_with_correct_processing,
            post_handler_function="async_tst_method_with_correct_processing",
        ),
    )

    @staticmethod
    async def async_tst_method_with_correct_processing(message: BaseOrchServMsg):
        CONST_LIST_ASYNC.append(-3)
        return message


class IncorrectTestFlowWithoutNameFlow(SyncFlow):
    steps_flow = FlowBuilder(
        FlowBlock(FirstBlock),
    )


class IncorrectTestFlowWithoutStepsFlow(SyncFlow):
    name_flow = "test_flow"


class IncorrectTestFlowWithIncorrectTypeSteps(SyncFlow):
    name_flow = "test_flow"
    steps_flow = FirstBlock()


class Test:
    pass


#
# class IncorrectTestFlowWithIncorrectFlowBlock(SyncFlow):
#     name_flow = "test_flow"
#     steps_flow = FlowBuilder(
#         Test,
#     )
