"""
Test Orchestrator
"""
from copy import deepcopy

import pytest

from orch_serv import AsyncOrchestrator, Orchestrator
from orch_serv.exc import (
    NoDateException,
    NotFoundDefaultError,
    UniqueNameException,
    WorkTypeMismatchException,
)
from tests.settings.settings_orchestrator import (
    settings_correct_orchestrator_async_blocks,
    settings_correct_orchestrator_async_flows,
    settings_correct_orchestrator_blocks,
    settings_correct_orchestrator_flows,
    settings_incorrect_async_blocks_not_unique_names,
    settings_incorrect_async_flows_not_unique_names,
    settings_incorrect_blocks_not_unique_names,
    settings_incorrect_flows_not_unique_names,
    settings_incorrect_flows_not_unique_names_option_2,
)
from tests.settings.settings_orchestrator.settings_orchestrator_msgs import (
    ASYNC_CORRECT_MSG_FIRST_FLOW_FIRST_BLOCK,
    ASYNC_CORRECT_MSG_FIRST_FLOW_SECOND_BLOCK,
    ASYNC_CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK,
    ASYNC_CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK,
    ASYNC_CORRECT_MSG_TO_FIRST_BLOCK,
    ASYNC_CORRECT_MSG_TO_SECOND_BLOCK,
    ASYNC_INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK,
    ASYNC_INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK2,
    ASYNC_INCORRECT_MSG_TO_BLOCK,
    CORRECT_MSG_FIRST_FLOW_FIRST_BLOCK,
    CORRECT_MSG_FIRST_FLOW_SECOND_BLOCK,
    CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK,
    CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK,
    CORRECT_MSG_TO_FIRST_BLOCK,
    CORRECT_MSG_TO_SECOND_BLOCK,
    INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK,
    INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK2,
    INCORRECT_MSG_TO_BLOCK,
)
from tests.settings.settings_test_block import CONST_LIST_ASYNC, CONST_LIST_SYNC


def test_init_orchestrator():
    """
    Test setup orchestrator
    :return:
    """
    with pytest.raises(NoDateException):
        Orchestrator()
    with pytest.raises(UniqueNameException):
        Orchestrator(flows=settings_incorrect_flows_not_unique_names)
    with pytest.raises(UniqueNameException):
        Orchestrator(flows=settings_incorrect_flows_not_unique_names_option_2)
    with pytest.raises(UniqueNameException):
        Orchestrator(
            flows=[
                settings_incorrect_flows_not_unique_names.flow,
                settings_incorrect_flows_not_unique_names.flow2,
            ]
        )
    with pytest.raises(NoDateException):
        Orchestrator(
            flows=[settings_incorrect_flows_not_unique_names.flow],
            flows_to_ignore=(
                settings_incorrect_flows_not_unique_names.names_file_to_ignore
            ),
        )
    with pytest.raises(UniqueNameException):
        Orchestrator(blocks=settings_incorrect_blocks_not_unique_names)
    with pytest.raises(UniqueNameException):
        Orchestrator(
            blocks=[
                settings_incorrect_blocks_not_unique_names.block,
                settings_incorrect_blocks_not_unique_names.block2,
            ]
        )
    with pytest.raises(NoDateException):
        Orchestrator(
            blocks=[settings_incorrect_blocks_not_unique_names.block],
            blocks_to_ignore=(
                settings_incorrect_blocks_not_unique_names.names_file_to_ignore
            ),
        )
    with pytest.raises(TypeError):
        Orchestrator(flows=settings_incorrect_blocks_not_unique_names)
    with pytest.raises(TypeError):
        Orchestrator(blocks=settings_incorrect_flows_not_unique_names)
    with pytest.raises(WorkTypeMismatchException):
        Orchestrator(
            flows=[settings_incorrect_async_flows_not_unique_names.flow],
        )
    with pytest.raises(WorkTypeMismatchException):
        Orchestrator(
            blocks=[settings_incorrect_async_blocks_not_unique_names.block],
        )

    with pytest.raises(NotFoundDefaultError):
        Orchestrator(blocks=settings_correct_orchestrator_blocks, default_block="test")
    with pytest.raises(NotFoundDefaultError):
        Orchestrator(flows=settings_correct_orchestrator_flows, default_flow="test")
    with pytest.raises(NotFoundDefaultError):
        Orchestrator(blocks=settings_correct_orchestrator_blocks, default_flow="test")
    with pytest.raises(NotFoundDefaultError):
        Orchestrator(flows=settings_correct_orchestrator_flows, default_block="test")


def test_init_async_orchestrator():
    """
    Test setup orchestrator
    :return:
    """
    with pytest.raises(NoDateException):
        AsyncOrchestrator()
    with pytest.raises(UniqueNameException):
        AsyncOrchestrator(flows=settings_incorrect_async_flows_not_unique_names)
    with pytest.raises(UniqueNameException):
        AsyncOrchestrator(
            flows=[
                settings_incorrect_async_flows_not_unique_names.flow,
                settings_incorrect_async_flows_not_unique_names.flow2,
            ]
        )
    with pytest.raises(NoDateException):
        AsyncOrchestrator(
            flows=[settings_incorrect_async_flows_not_unique_names.flow],
            flows_to_ignore=(
                settings_incorrect_async_flows_not_unique_names.names_file_to_ignore
            ),
        )
    with pytest.raises(UniqueNameException):
        AsyncOrchestrator(blocks=settings_incorrect_async_blocks_not_unique_names)
    with pytest.raises(UniqueNameException):
        AsyncOrchestrator(
            blocks=[
                settings_incorrect_async_blocks_not_unique_names.block,
                settings_incorrect_async_blocks_not_unique_names.block2,
            ]
        )
    with pytest.raises(NoDateException):
        AsyncOrchestrator(
            blocks=[settings_incorrect_async_blocks_not_unique_names.block],
            blocks_to_ignore=(
                settings_incorrect_async_blocks_not_unique_names.names_file_to_ignore
            ),
        )
    with pytest.raises(TypeError):
        AsyncOrchestrator(flows=settings_incorrect_async_blocks_not_unique_names)
    with pytest.raises(TypeError):
        AsyncOrchestrator(blocks=settings_incorrect_async_flows_not_unique_names)
    with pytest.raises(WorkTypeMismatchException):
        AsyncOrchestrator(
            flows=[settings_incorrect_flows_not_unique_names.flow],
        )
    with pytest.raises(WorkTypeMismatchException):
        AsyncOrchestrator(
            blocks=[settings_incorrect_blocks_not_unique_names.block],
        )

    with pytest.raises(NotFoundDefaultError):
        AsyncOrchestrator(
            blocks=settings_correct_orchestrator_async_blocks, default_block="test"
        )
    with pytest.raises(NotFoundDefaultError):
        AsyncOrchestrator(
            flows=settings_correct_orchestrator_async_flows, default_flow="test"
        )
    with pytest.raises(NotFoundDefaultError):
        AsyncOrchestrator(
            blocks=settings_correct_orchestrator_async_blocks, default_flow="test"
        )
    with pytest.raises(NotFoundDefaultError):
        AsyncOrchestrator(
            flows=settings_correct_orchestrator_async_flows, default_block="test"
        )


def test_orchestrator_handler():
    CONST_LIST_SYNC.clear()
    orchestrator = Orchestrator(
        flows=settings_correct_orchestrator_flows,
        blocks=settings_correct_orchestrator_blocks,
    )
    orchestrator.handle(deepcopy(CORRECT_MSG_FIRST_FLOW_FIRST_BLOCK))
    assert CONST_LIST_SYNC == [-3, 1, -1]
    orchestrator.handle(deepcopy(CORRECT_MSG_FIRST_FLOW_SECOND_BLOCK))
    assert CONST_LIST_SYNC == [-3, 1, -1, -1, 2, -3]
    CONST_LIST_SYNC.clear()

    res = orchestrator.handle(deepcopy(CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK))
    assert CONST_LIST_SYNC == [-3, 1, -1]
    assert res is None
    res = orchestrator.handle(deepcopy(CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK))
    assert CONST_LIST_SYNC == [-3, 1, -1, -1, 2, -3]
    assert res is None

    CONST_LIST_SYNC.clear()
    res = orchestrator.handle(CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK, is_force_return=True)
    assert CONST_LIST_SYNC == [-3, 1, -1]
    assert res == CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK
    res = orchestrator.handle(
        CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK, is_force_return=True
    )
    assert CONST_LIST_SYNC == [-3, 1, -1, -1, 2, -3]
    assert res == CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK
    CONST_LIST_SYNC.clear()

    res = orchestrator.handle(CORRECT_MSG_TO_FIRST_BLOCK, is_force_return=True)
    assert CONST_LIST_SYNC == [1]
    assert res is CORRECT_MSG_TO_FIRST_BLOCK
    res = orchestrator.handle(
        CORRECT_MSG_TO_SECOND_BLOCK,
    )
    assert CONST_LIST_SYNC == [1, 2]
    assert res is None
    CONST_LIST_SYNC.clear()

    res = orchestrator.handle(INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK)
    assert res == INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK
    assert CONST_LIST_SYNC == []
    res = orchestrator.handle(INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK2)
    assert res == INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK2
    assert CONST_LIST_SYNC == []

    orchestrator = Orchestrator(
        flows=settings_correct_orchestrator_flows,
        blocks=settings_correct_orchestrator_blocks,
        default_block=settings_correct_orchestrator_blocks.FirstBlock.name_block,
        default_flow=settings_correct_orchestrator_flows.TestFlow.name_flow,
    )
    res = orchestrator.handle(INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK)
    assert CONST_LIST_SYNC == [-1, 2, -3]
    assert res is None
    res = orchestrator.handle(INCORRECT_MSG_TO_BLOCK)
    assert CONST_LIST_SYNC == [-1, 2, -3, 1]
    assert res is None

    with pytest.raises(TypeError):
        orchestrator.handle(CONST_LIST_SYNC)


@pytest.mark.asyncio
async def test_async_orchestrator_handler():
    CONST_LIST_ASYNC.clear()
    orchestrator = AsyncOrchestrator(
        blocks=settings_correct_orchestrator_async_blocks,
        flows=settings_correct_orchestrator_async_flows,
    )

    await orchestrator.handle(deepcopy(ASYNC_CORRECT_MSG_FIRST_FLOW_FIRST_BLOCK))
    assert CONST_LIST_ASYNC == [-3, 1, -1]
    await orchestrator.handle(deepcopy(ASYNC_CORRECT_MSG_FIRST_FLOW_SECOND_BLOCK))
    assert CONST_LIST_ASYNC == [-3, 1, -1, -1, 2, -3]
    CONST_LIST_ASYNC.clear()

    res = await orchestrator.handle(deepcopy(ASYNC_CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK))
    assert CONST_LIST_ASYNC == [-3, 1, -1]
    assert res is None
    res = await orchestrator.handle(
        deepcopy(ASYNC_CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK)
    )
    assert CONST_LIST_ASYNC == [-3, 1, -1, -1, 2, -3]
    assert res is None

    CONST_LIST_ASYNC.clear()
    res = await orchestrator.handle(
        ASYNC_CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK, is_force_return=True
    )
    assert CONST_LIST_ASYNC == [-3, 1, -1]
    assert res == ASYNC_CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK
    res = await orchestrator.handle(
        ASYNC_CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK, is_force_return=True
    )
    assert CONST_LIST_ASYNC == [-3, 1, -1, -1, 2, -3]
    assert res == ASYNC_CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK
    CONST_LIST_ASYNC.clear()
    #
    res = await orchestrator.handle(
        ASYNC_CORRECT_MSG_TO_FIRST_BLOCK, is_force_return=True
    )
    assert CONST_LIST_ASYNC == [1]
    assert res is ASYNC_CORRECT_MSG_TO_FIRST_BLOCK
    res = await orchestrator.handle(
        ASYNC_CORRECT_MSG_TO_SECOND_BLOCK,
    )
    assert CONST_LIST_ASYNC == [1, 2]
    assert res is None
    CONST_LIST_ASYNC.clear()

    res = await orchestrator.handle(ASYNC_INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK)
    assert res == ASYNC_INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK
    assert CONST_LIST_ASYNC == []
    res = await orchestrator.handle(ASYNC_INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK2)
    assert res == ASYNC_INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK2
    assert CONST_LIST_ASYNC == []
    #
    orchestrator = AsyncOrchestrator(
        flows=settings_correct_orchestrator_async_flows,
        blocks=settings_correct_orchestrator_async_blocks,
        default_block=(
            settings_correct_orchestrator_async_blocks.FirstAsyncBlock.name_block
        ),
        default_flow=settings_correct_orchestrator_async_flows.TestAsyncFlow.name_flow,
    )
    res = await orchestrator.handle(ASYNC_INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK)
    assert CONST_LIST_ASYNC == [-1, 2, -3]
    assert res is None
    res = await orchestrator.handle(ASYNC_INCORRECT_MSG_TO_BLOCK)
    assert CONST_LIST_ASYNC == [-1, 2, -3, 1]
    assert res is None

    with pytest.raises(TypeError):
        await orchestrator.handle(CONST_LIST_ASYNC)
