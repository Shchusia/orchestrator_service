from copy import deepcopy

import pytest

from orch_serv import FlowBlock, FlowBuilder, SyncFlow
from orch_serv.exc import FlowBlockException, FlowBuilderException
from tests.settings.settings_test_block import (
    CONST_LIST_ASYNC,
    CONST_LIST_SYNC,
    MSG_TO_PROCESS_IN_FIRST_BLOCK,
    MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK,
    MSG_TO_PROCESS_IN_SECOND_BLOCK,
)
from tests.settings.settings_test_flow import (
    IncorrectTestFlowWithIncorrectTypeSteps,
    IncorrectTestFlowWithoutNameFlow,
    IncorrectTestFlowWithoutStepsFlow,
    Test,
    TestAsyncFlow,
    TestFlow,
)


def test_build_flow():
    with pytest.raises(NotImplementedError):
        IncorrectTestFlowWithoutNameFlow()
    with pytest.raises(NotImplementedError):
        IncorrectTestFlowWithoutStepsFlow()
    with pytest.raises(TypeError):
        IncorrectTestFlowWithIncorrectTypeSteps()
    with pytest.raises(FlowBuilderException):

        class IncorrectTestFlowWithIncorrectFlowBlock(SyncFlow):
            name_flow = "test_flow"
            steps_flow = FlowBuilder(
                Test,
            )

    with pytest.raises(FlowBlockException):

        class IncorrectTestFlowWithIncorrectBlockInFlowBlock(SyncFlow):
            name_flow = "test_flow"
            steps_flow = FlowBuilder(
                FlowBlock(Test),
            )


def test_flow_handling():
    """
    test is correct handling flow messages
    :return:
    """
    flow = TestFlow()
    flow.to_go_with_the_flow(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))

    assert CONST_LIST_SYNC == [-3, 1, -1]
    flow.to_go_with_the_flow(deepcopy(MSG_TO_PROCESS_IN_SECOND_BLOCK))
    assert CONST_LIST_SYNC == [-3, 1, -1, -1, 2, -3]


@pytest.mark.asyncio
async def test_async_flow_handling():
    """
    test is correct handling async flow messages
    :return:
    """
    flow = TestAsyncFlow()
    await flow.to_go_with_the_flow(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))

    assert CONST_LIST_ASYNC == [-3, 1, -1]
    await flow.to_go_with_the_flow(deepcopy(MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK))
    assert CONST_LIST_ASYNC == [-3, 1, -1, -1, 2, -3]
