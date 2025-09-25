"""
Test Orchestrator
"""
import inspect
from copy import deepcopy
from logging import getLogger

import pytest

from orch_serv import AsyncOrchestrator, SyncOrchestrator
from orch_serv.exc import (
    NoDateException,
    NotFoundDefaultError,
    UniqueNameException,
    WorkTypeMismatchException,
    WrongTypeException,
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
    settings_incorrect_flows_not_unique_names_option_2, settings_correct_for_ignore_flows,
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
    CORRECT_EMPTY_MSG,
    CORRECT_MSG_FIRST_FLOW_FIRST_BLOCK,
    CORRECT_MSG_FIRST_FLOW_SECOND_BLOCK,
    CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK,
    CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK,
    CORRECT_MSG_TO_ASYNC_BLOCK_WITH_EXCEPTION,
    CORRECT_MSG_TO_BLOCK_WITH_EXCEPTION,
    CORRECT_MSG_TO_FIRST_BLOCK,
    CORRECT_MSG_TO_SECOND_BLOCK,
    INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK,
    INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK2,
    INCORRECT_MSG_TO_BLOCK,
    INCORRECT_MSG_TO_NotExistedBLOCK,
)
from tests.settings.settings_test_block import (
    CONST_LIST_ASYNC,
    CONST_LIST_SYNC,
    FirstBlock,
    SecondBlock,
)
from tests.settings.settings_test_flow import SecondTestFlow, TestFlow


def test_init_orchestrator():
    """
    Test setup orchestrator
    :return:
    """
    with pytest.raises(NoDateException):
        SyncOrchestrator()
    with pytest.raises(UniqueNameException):
        SyncOrchestrator(flows=settings_incorrect_flows_not_unique_names)
    with pytest.raises(UniqueNameException):

        class Orchestrator(SyncOrchestrator):
            flows = settings_incorrect_flows_not_unique_names

        Orchestrator()
    with pytest.raises(UniqueNameException):
        SyncOrchestrator(flows=settings_incorrect_flows_not_unique_names_option_2)
    with pytest.raises(UniqueNameException):

        class Orchestrator(SyncOrchestrator):
            flows = settings_incorrect_flows_not_unique_names_option_2

        Orchestrator()
    with pytest.raises(UniqueNameException):
        SyncOrchestrator(
            flows=[
                settings_incorrect_flows_not_unique_names.flow,
                settings_incorrect_flows_not_unique_names.flow2,
            ]
        )
    with pytest.raises(UniqueNameException):

        class Orchestrator(SyncOrchestrator):
            flows = [
                settings_incorrect_flows_not_unique_names.flow,
                settings_incorrect_flows_not_unique_names.flow2,
            ]

        Orchestrator()
    with pytest.raises(NoDateException):
        SyncOrchestrator(
            flows=[settings_incorrect_flows_not_unique_names.flow],
            flows_to_ignore=(
                settings_incorrect_flows_not_unique_names.names_file_to_ignore
            ),
        )
    # with pytest.raises(NoDateException):
    class Orchestrator(SyncOrchestrator):
        flows = [settings_correct_for_ignore_flows.TestFlow, settings_correct_for_ignore_flows.SecondTestFlow]
    so = Orchestrator(
            # flows=[settings_correct_for_ignore_flows.TestFlow, settings_correct_for_ignore_flows.SecondTestFlow],
            flows_to_ignore=(
                settings_correct_for_ignore_flows.names_file_to_ignore
            ),
        )
    assert len(so.get_list_flows()) == 1
    with pytest.raises(NoDateException):

        class Orchestrator(SyncOrchestrator):
            flows = [settings_incorrect_flows_not_unique_names.flow]

        Orchestrator(
            flows_to_ignore=(
                settings_incorrect_flows_not_unique_names.names_file_to_ignore
            ),
        )
    with pytest.raises(UniqueNameException):
        SyncOrchestrator(blocks=settings_incorrect_blocks_not_unique_names)
    with pytest.raises(UniqueNameException):

        class Orchestrator(SyncOrchestrator):
            blocks = settings_incorrect_blocks_not_unique_names

        Orchestrator()

    with pytest.raises(UniqueNameException):

        class Orchestrator(SyncOrchestrator):
            blocks = [
                settings_incorrect_blocks_not_unique_names.block,
                settings_incorrect_blocks_not_unique_names.block2,
            ]

        Orchestrator()
    with pytest.raises(NoDateException):
        SyncOrchestrator(
            blocks=[settings_incorrect_blocks_not_unique_names.block],
            blocks_to_ignore=(
                settings_incorrect_blocks_not_unique_names.names_file_to_ignore
            ),
        )
    with pytest.raises(NoDateException):

        class Orchestrator(SyncOrchestrator):
            blocks = [settings_incorrect_blocks_not_unique_names.block]

        Orchestrator(
            blocks_to_ignore=(
                settings_incorrect_blocks_not_unique_names.names_file_to_ignore
            ),
        )
    with pytest.raises(TypeError):
        SyncOrchestrator(flows=settings_incorrect_blocks_not_unique_names)
    with pytest.raises(TypeError):

        class Orchestrator(SyncOrchestrator):
            flows = settings_incorrect_blocks_not_unique_names

        Orchestrator()
    with pytest.raises(TypeError):
        SyncOrchestrator(blocks=settings_incorrect_flows_not_unique_names)
    with pytest.raises(TypeError):

        class Orchestrator(SyncOrchestrator):
            blocks = settings_incorrect_flows_not_unique_names

        Orchestrator()
    with pytest.raises(WorkTypeMismatchException):
        SyncOrchestrator(
            flows=[settings_incorrect_async_flows_not_unique_names.flow],
        )
    with pytest.raises(WorkTypeMismatchException):

        class Orchestrator(SyncOrchestrator):
            flows = [settings_incorrect_async_flows_not_unique_names.flow]

        Orchestrator()

    with pytest.raises(WorkTypeMismatchException):
        SyncOrchestrator(
            blocks=[settings_incorrect_async_blocks_not_unique_names.block],
        )

    with pytest.raises(WorkTypeMismatchException):

        class Orchestrator(SyncOrchestrator):
            blocks = [settings_incorrect_async_blocks_not_unique_names.block]

        Orchestrator()

    with pytest.raises(NotFoundDefaultError):
        SyncOrchestrator(
            blocks=settings_correct_orchestrator_blocks, default_block="test"
        )
    with pytest.raises(NotFoundDefaultError):

        class Orchestrator(SyncOrchestrator):
            blocks = settings_correct_orchestrator_blocks

        Orchestrator(default_block="test")
    with pytest.raises(NotFoundDefaultError):
        SyncOrchestrator(flows=settings_correct_orchestrator_flows, default_flow="test")
    with pytest.raises(NotFoundDefaultError):

        class Orchestrator(SyncOrchestrator):
            flows = settings_correct_orchestrator_flows

        Orchestrator(default_flow="test")
    with pytest.raises(NotFoundDefaultError):
        SyncOrchestrator(
            blocks=settings_correct_orchestrator_blocks, default_flow="test"
        )
    with pytest.raises(NotFoundDefaultError):
        SyncOrchestrator(
            blocks=settings_correct_orchestrator_blocks, default_flow="test"
        )
    with pytest.raises(NotFoundDefaultError):

        class Orchestrator(SyncOrchestrator):
            flows = settings_correct_orchestrator_flows

        Orchestrator(default_block="test")
    SyncOrchestrator(
        flows=[TestFlow, SecondTestFlow()],
        blocks=[FirstBlock, SecondBlock],
        blocks_to_ignore=[settings_correct_orchestrator_blocks.FirstBlock.__name__],
        # flows_to_ignore=[settings_correct_orchestrator_flows.TestFlow.__name__],
        flows_to_ignore=[TestFlow.name_flow],
    )
    SyncOrchestrator(
        flows=settings_correct_orchestrator_flows,
        blocks=[FirstBlock, SecondBlock()],
        blocks_to_ignore=[settings_correct_orchestrator_blocks.FirstBlock.__name__],
        # flows_to_ignore=[settings_correct_orchestrator_flows.TestFlow.__name__],
        flows_to_ignore=[TestFlow.name_flow],
    )
    with pytest.raises(TypeError):
        SyncOrchestrator(
            blocks=settings_correct_orchestrator_flows,
            flows=[FirstBlock, SecondBlock],
            blocks_to_ignore=[settings_correct_orchestrator_blocks.FirstBlock.__name__],
            # flows_to_ignore=[settings_correct_orchestrator_flows.TestFlow.__name__],
            flows_to_ignore=[TestFlow.name_flow],
        )
    with pytest.raises(WrongTypeException):
        SyncOrchestrator(
            blocks=(FirstBlock, SecondBlock),
            flows=settings_correct_orchestrator_flows,
            blocks_to_ignore=[settings_correct_orchestrator_blocks.FirstBlock.__name__],
            # flows_to_ignore=[settings_correct_orchestrator_flows.TestFlow.__name__],
            flows_to_ignore=[TestFlow.name_flow],
        )
    with pytest.raises(NoDateException):
        SyncOrchestrator(
            blocks=[FirstBlock, SecondBlock],
            flows=[TestFlow],
            blocks_to_ignore=[settings_correct_orchestrator_blocks.FirstBlock.__name__],
            # flows_to_ignore=[settings_correct_orchestrator_flows.TestFlow.__name__],
            flows_to_ignore=[TestFlow.name_flow],
        )
    with pytest.raises(UniqueNameException):
        SyncOrchestrator(
            blocks=[FirstBlock, FirstBlock()],
            flows=[TestFlow],
        )


def test_init_async_orchestrator():
    """
    Test setup async orchestrator
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
    with pytest.raises(NoDateException):

        class Orchestrator(AsyncOrchestrator):
            pass

        Orchestrator()
    with pytest.raises(UniqueNameException):

        class Orchestrator(AsyncOrchestrator):
            flows = settings_incorrect_async_flows_not_unique_names

        Orchestrator()

    with pytest.raises(UniqueNameException):

        class Orchestrator(AsyncOrchestrator):
            flows = [
                settings_incorrect_async_flows_not_unique_names.flow,
                settings_incorrect_async_flows_not_unique_names.flow2,
            ]

        Orchestrator()

    with pytest.raises(NoDateException):

        class Orchestrator(AsyncOrchestrator):
            flows = [settings_incorrect_async_flows_not_unique_names.flow]

        Orchestrator(
            flows_to_ignore=(
                settings_incorrect_async_flows_not_unique_names.names_file_to_ignore
            ),
        )
    with pytest.raises(UniqueNameException):

        class Orchestrator(AsyncOrchestrator):
            blocks = settings_incorrect_async_blocks_not_unique_names

        Orchestrator()
    with pytest.raises(UniqueNameException):

        class Orchestrator(AsyncOrchestrator):
            blocks = [
                settings_incorrect_async_blocks_not_unique_names.block,
                settings_incorrect_async_blocks_not_unique_names.block2,
            ]

        Orchestrator()

    with pytest.raises(NoDateException):

        class Orchestrator(AsyncOrchestrator):
            blocks = [settings_incorrect_async_blocks_not_unique_names.block]

        Orchestrator(
            blocks_to_ignore=(
                settings_incorrect_async_blocks_not_unique_names.names_file_to_ignore
            ),
        )
    with pytest.raises(TypeError):

        class Orchestrator(AsyncOrchestrator):
            flows = settings_incorrect_async_blocks_not_unique_names

        Orchestrator()
    with pytest.raises(TypeError):

        class Orchestrator(AsyncOrchestrator):
            blocks = settings_incorrect_async_flows_not_unique_names

        Orchestrator()
    with pytest.raises(WorkTypeMismatchException):

        class Orchestrator(AsyncOrchestrator):
            flows = [settings_incorrect_flows_not_unique_names.flow]

        Orchestrator()
    with pytest.raises(WorkTypeMismatchException):

        class Orchestrator(AsyncOrchestrator):
            blocks = [settings_incorrect_blocks_not_unique_names.block]

        Orchestrator()

    with pytest.raises(NotFoundDefaultError):

        class Orchestrator(AsyncOrchestrator):
            blocks = settings_correct_orchestrator_async_blocks

        Orchestrator(default_block="test")
    with pytest.raises(NotFoundDefaultError):

        class Orchestrator(AsyncOrchestrator):
            flows = settings_correct_orchestrator_async_flows

        Orchestrator(default_flow="test")
    with pytest.raises(NotFoundDefaultError):

        class Orchestrator(AsyncOrchestrator):
            blocks = settings_correct_orchestrator_async_blocks

        Orchestrator(default_flow="test")
    with pytest.raises(NotFoundDefaultError):

        class Orchestrator(AsyncOrchestrator):
            flows = settings_correct_orchestrator_async_flows

        Orchestrator(default_block="test")


def test_orchestrator_handler():
    """
    Test orchestrator handling msgs
    :return:
    """
    CONST_LIST_SYNC.clear()
    orchestrator = SyncOrchestrator(
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

    orchestrator = SyncOrchestrator(
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
    list_blocks = list()
    list_flows = list()
    for _, clazz in inspect.getmembers(
        settings_correct_orchestrator_blocks, inspect.isclass
    ):
        list_blocks.append(clazz.name_block)
    for _, clazz in inspect.getmembers(
        settings_correct_orchestrator_flows, inspect.isclass
    ):
        list_flows.append(clazz.name_flow)
    assert orchestrator.get_list_blocks().sort() == list_blocks.sort()
    assert orchestrator.get_list_flows().sort() == list_flows.sort()

    orchestrator = SyncOrchestrator(
        flows=settings_correct_orchestrator_flows,
        blocks=settings_correct_orchestrator_blocks,
    )
    res = orchestrator.handle(INCORRECT_MSG_TO_NotExistedBLOCK)
    assert INCORRECT_MSG_TO_NotExistedBLOCK == res
    orchestrator.handle(deepcopy(CORRECT_MSG_TO_SECOND_BLOCK))
    orchestrator.handle(deepcopy(CORRECT_MSG_TO_SECOND_BLOCK))
    res = orchestrator.handle(deepcopy(CORRECT_MSG_TO_BLOCK_WITH_EXCEPTION))
    assert res == CORRECT_MSG_TO_BLOCK_WITH_EXCEPTION
    res = orchestrator.handle(deepcopy(CORRECT_EMPTY_MSG))
    assert res == CORRECT_EMPTY_MSG


@pytest.mark.asyncio
async def test_async_orchestrator_handler():
    """
    Test orchestrator handling msgs
    :return:
    """
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

    list_blocks = list()
    list_flows = list()
    for _, clazz in inspect.getmembers(
        settings_correct_orchestrator_async_blocks, inspect.isclass
    ):
        list_blocks.append(clazz.name_block)
    for _, clazz in inspect.getmembers(
        settings_correct_orchestrator_async_flows, inspect.isclass
    ):
        list_flows.append(clazz.name_flow)
    assert orchestrator.get_list_blocks().sort() == list_blocks.sort()
    assert orchestrator.get_list_flows().sort() == list_flows.sort()

    orchestrator = AsyncOrchestrator(
        flows=settings_correct_orchestrator_async_flows,
        blocks=settings_correct_orchestrator_async_blocks,
    )
    res = await orchestrator.handle(INCORRECT_MSG_TO_NotExistedBLOCK)
    assert INCORRECT_MSG_TO_NotExistedBLOCK == res
    await orchestrator.handle(deepcopy(ASYNC_CORRECT_MSG_TO_SECOND_BLOCK))
    await orchestrator.handle(deepcopy(ASYNC_CORRECT_MSG_TO_SECOND_BLOCK))
    res = await orchestrator.handle(deepcopy(CORRECT_MSG_TO_ASYNC_BLOCK_WITH_EXCEPTION))
    assert res == CORRECT_MSG_TO_ASYNC_BLOCK_WITH_EXCEPTION
    res = await orchestrator.handle(deepcopy(CORRECT_EMPTY_MSG))
    assert res == CORRECT_EMPTY_MSG
