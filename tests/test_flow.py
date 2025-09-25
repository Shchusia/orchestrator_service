from copy import deepcopy

import pytest
from charset_normalizer.md import getLogger

from orch_serv import FlowBlock, FlowBuilder, SyncFlow
from orch_serv.exc import (
    FlowBlockException,
    FlowBuilderException,
    NotUniqueBlockInFlowError,
    WorkTypeMismatchException,
)
from tests.settings.settings_test_block import (
    CONST_LIST_ASYNC,
    CONST_LIST_SYNC,
    MSG_TO_PROCESS_IN_FIRST_BLOCK,
    MSG_TO_PROCESS_IN_FORTH_ASYNC_BLOCK,
    MSG_TO_PROCESS_IN_FORTH_SYNC_BLOCK,
    MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK,
    MSG_TO_PROCESS_IN_SECOND_BLOCK,
    MSG_TO_PROCESS_IN_THIRD_ASYNC_BLOCK,
    MSG_TO_PROCESS_IN_THIRD_SYNC_BLOCK,
    FirstAsyncBlock,
    FirstBlock,
)
from tests.settings.settings_test_flow import (
    CorrectTestFlowWithDublicatBlocks,
    FourthTestAsyncFlow,
    FourthTestSyncFlow,
    IncorrectTestAsyncFlowUseSyncBlock,
    IncorrectTestFlowUseAsyncBlock,
    IncorrectTestFlowWithDublicatBlocks,
    IncorrectTestFlowWithIncorrectTypeSteps,
    IncorrectTestFlowWithoutNameFlow,
    IncorrectTestFlowWithoutStepsFlow,
    Test,
    TestAsyncFlow,
    TestFlow,
    ThirdTestAsyncFlow,
    ThirdTestSyncFlow,
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



    with pytest.raises(WorkTypeMismatchException):
        IncorrectTestFlowUseAsyncBlock()
    with pytest.raises(WorkTypeMismatchException):
        IncorrectTestAsyncFlowUseSyncBlock()
    with pytest.raises(NotUniqueBlockInFlowError):
        IncorrectTestFlowWithDublicatBlocks()

    ctf = CorrectTestFlowWithDublicatBlocks()  # noqa
    getLogger(__name__).warning(ctf.steps_flow)
    getLogger(__name__).warning(ctf)
    ctf.steps_flow = 1
    getLogger(__name__).warning(ctf.steps_flow)


def test_flow_handling():
    """
    test is correct handling flow messages
    :return:
    """
    CONST_LIST_SYNC.clear()
    flow = TestFlow()
    flow.to_go_with_the_flow(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))

    assert CONST_LIST_SYNC == [-3, 1, -1]
    flow.to_go_with_the_flow(deepcopy(MSG_TO_PROCESS_IN_SECOND_BLOCK))
    assert CONST_LIST_SYNC == [-3, 1, -1, -1, 2, -3]

    CONST_LIST_SYNC.clear()
    flow_3 = ThirdTestSyncFlow()
    flow_4 = FourthTestSyncFlow()
    flow_3.to_go_with_the_flow(MSG_TO_PROCESS_IN_THIRD_SYNC_BLOCK)
    assert CONST_LIST_SYNC == [-1, 3, -1]
    flow_3.to_go_with_the_flow(MSG_TO_PROCESS_IN_THIRD_SYNC_BLOCK)
    assert CONST_LIST_SYNC == [-1, 3, -1, -3]
    flow_4.to_go_with_the_flow(MSG_TO_PROCESS_IN_FORTH_SYNC_BLOCK)
    assert CONST_LIST_SYNC == [-1, 3, -1, -3, -1, 4]


@pytest.mark.asyncio
async def test_async_flow_handling():
    """
    test is correct handling async flow messages
    :return:
    """
    CONST_LIST_ASYNC.clear()
    flow = TestAsyncFlow()
    await flow.to_go_with_the_flow(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))

    assert CONST_LIST_ASYNC == [-3, 1, -1]
    await flow.to_go_with_the_flow(deepcopy(MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK))
    assert CONST_LIST_ASYNC == [-3, 1, -1, -1, 2, -3]

    CONST_LIST_ASYNC.clear()
    flow_3 = ThirdTestAsyncFlow()
    flow_4 = FourthTestAsyncFlow()
    await flow_3.to_go_with_the_flow(MSG_TO_PROCESS_IN_THIRD_ASYNC_BLOCK)
    assert CONST_LIST_ASYNC == [-1, 3, -1]
    await flow_3.to_go_with_the_flow(MSG_TO_PROCESS_IN_THIRD_ASYNC_BLOCK)
    print(CONST_LIST_ASYNC)
    assert CONST_LIST_ASYNC == [-1, 3, -1, -3]
    await flow_4.to_go_with_the_flow(MSG_TO_PROCESS_IN_FORTH_ASYNC_BLOCK)
    assert CONST_LIST_ASYNC == [-1, 3, -1, -3, -1, 4]
    assert flow_4.get_steps() == "fourth async block -> end"


def test_flow_block():
    fb = FlowBlock(FirstBlock)
    FlowBlock(FirstBlock())
    FlowBlock(FirstAsyncBlock)
    FlowBlock(FirstAsyncBlock())
    with pytest.raises(FlowBlockException):
        FlowBlock(ThirdTestAsyncFlow)
    with pytest.raises(TypeError):
        fb.init_block(ThirdTestAsyncFlow)
    with pytest.raises(TypeError):
        fb.init_block(FirstBlock)
