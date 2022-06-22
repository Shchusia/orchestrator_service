"""
Tests for block
"""
from copy import deepcopy
from typing import Optional

import pytest

from orch_serv import BaseOrchServMsg
from orch_serv.exc import OrchServError
from orch_serv.orchestrator.block.base_block import AsyncBaseBlock, SyncBaseBlock
from tests.settings.settings_test_block import (
    CONST_LIST_ASYNC,
    CONST_LIST_SYNC,
    MSG_TO_PROCESS_IN_FIRST_BLOCK,
    MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK,
    MSG_TO_PROCESS_IN_SECOND_BLOCK,
    FirstAsyncBlock,
    FirstBlock,
    OtherClassForBlocks,
    OtherClassForBlocksWithErrorInTimeInit,
    OtherClassForBlocksWithErrorInTimeInitWithoutArguments,
    SecondAsyncBlock,
    SecondBlock,
    async_tst_method_with_correct_processing,
    async_tst_method_with_incorrect_processing,
    tst_method_with_correct_processing,
    tst_method_with_incorrect_processing,
)


def test_block():
    block_f = FirstBlock()
    block_s = SecondBlock()

    with pytest.raises(TypeError):
        block_f.set_next(FirstAsyncBlock())  # noqa
    with pytest.raises(TypeError):
        block_f.set_next(FirstAsyncBlock)  # noqa
    with pytest.raises(TypeError):
        block_f.set_next(OtherClassForBlocks)  # noqa
    with pytest.raises(TypeError):
        block_f.set_next(OtherClassForBlocksWithErrorInTimeInit)  # noqa
    with pytest.raises(OrchServError):
        block_f.set_next(OtherClassForBlocksWithErrorInTimeInitWithoutArguments)  # noqa
    with pytest.raises(TypeError):
        block_s.set_next(FirstAsyncBlock())  # noqa
    with pytest.raises(TypeError):
        block_s.set_next(FirstAsyncBlock)  # noqa
    with pytest.raises(TypeError):
        block_s.set_next(OtherClassForBlocks)  # noqa
    with pytest.raises(TypeError):
        block_s.set_next(OtherClassForBlocksWithErrorInTimeInit)  # noqa
    with pytest.raises(OrchServError):
        block_s.set_next(OtherClassForBlocksWithErrorInTimeInitWithoutArguments)  # noqa

    block_f.set_next(block_s)

    assert block_f.get_list_flow() == "first block -> second block -> end"
    block_f.handle(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))
    assert CONST_LIST_SYNC == [1]
    block_f.handle(deepcopy(MSG_TO_PROCESS_IN_SECOND_BLOCK))
    assert CONST_LIST_SYNC == [1, 2]

    block_f = FirstBlock(
        pre_handler_function=tst_method_with_correct_processing,
        post_handler_function=tst_method_with_correct_processing,
    )
    block_s = SecondBlock(
        pre_handler_function=tst_method_with_correct_processing,
        post_handler_function=tst_method_with_correct_processing,
    )
    block_f.set_next(block_s)

    block_f.handle(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))
    assert CONST_LIST_SYNC == [1, 2, -1, 1, -1]
    block_f.handle(deepcopy(MSG_TO_PROCESS_IN_SECOND_BLOCK))
    assert CONST_LIST_SYNC == [1, 2, -1, 1, -1, -1, 2, -1]

    block_f = FirstBlock(
        pre_handler_function=tst_method_with_incorrect_processing,
        post_handler_function=tst_method_with_correct_processing,
    )
    block_s = SecondBlock(
        pre_handler_function=tst_method_with_incorrect_processing,
        post_handler_function=tst_method_with_correct_processing,
    )
    block_f.set_next(block_s)
    block_f.handle(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))
    assert CONST_LIST_SYNC == [1, 2, -1, 1, -1, -1, 2, -1, -2]
    block_f.handle(deepcopy(MSG_TO_PROCESS_IN_SECOND_BLOCK))
    assert CONST_LIST_SYNC == [1, 2, -1, 1, -1, -1, 2, -1, -2, -2]

    assert block_f.get_next() == block_s
    assert block_s.get_next() is None

    CONST_LIST_SYNC.clear()
    assert block_f.name_block == FirstBlock.name_block
    assert block_s.name_block == SecondBlock.name_block

    block_f.process(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))
    assert CONST_LIST_SYNC == [1]
    block_s.process(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))
    assert CONST_LIST_SYNC == [1, 2]

    class TestClass(SyncBaseBlock):
        pass

    class TestSecondClass(SyncBaseBlock):
        def set_next(self, handler: SyncBaseBlock) -> SyncBaseBlock:
            pass

        def get_next(self) -> SyncBaseBlock:
            pass

        def get_list_flow(self) -> str:
            pass

        def handle(self, message: BaseOrchServMsg) -> None:
            pass

        def process(self, message: BaseOrchServMsg) -> Optional[BaseOrchServMsg]:
            pass

    with pytest.raises(TypeError):
        TestClass()
    with pytest.raises(NotImplementedError):
        TestSecondClass().name_block
    with pytest.raises(NotImplementedError):
        TestSecondClass().pre_handler_function
    with pytest.raises(NotImplementedError):
        TestSecondClass().post_handler_function

    def test_funct(msg):
        pass

    block_f = FirstBlock()
    block_f.pre_handler_function = test_funct
    assert block_f.pre_handler_function == test_funct
    block_f.post_handler_function = test_funct
    assert block_f.post_handler_function == test_funct
    block_f = FirstBlock()

    block_f.pre_handler_function = ""
    block_f.post_handler_function = ""
    assert block_f.pre_handler_function is None
    assert block_f.post_handler_function is None

    with pytest.raises(TypeError):
        block_f.pre_handler_function = 1
    with pytest.raises(TypeError):
        block_f.pre_handler_function = "sad"
    with pytest.raises(TypeError):
        block_f.post_handler_function = 1
    with pytest.raises(TypeError):
        block_f.post_handler_function = "sad"


@pytest.mark.asyncio
async def test_async_block():
    block_f = FirstAsyncBlock()
    block_s = SecondAsyncBlock()

    with pytest.raises(TypeError):
        block_f.set_next(FirstBlock())  # noqa
    with pytest.raises(TypeError):
        block_f.set_next(FirstBlock)  # noqa
    with pytest.raises(TypeError):
        block_f.set_next(OtherClassForBlocks)  # noqa
    with pytest.raises(TypeError):
        block_f.set_next(OtherClassForBlocksWithErrorInTimeInit)  # noqa
    with pytest.raises(OrchServError):
        block_f.set_next(OtherClassForBlocksWithErrorInTimeInitWithoutArguments)  # noqa
    with pytest.raises(TypeError):
        block_s.set_next(FirstBlock())  # noqa
    with pytest.raises(TypeError):
        block_s.set_next(FirstBlock)  # noqa
    with pytest.raises(TypeError):
        block_s.set_next(OtherClassForBlocks)  # noqa
    with pytest.raises(TypeError):
        block_s.set_next(OtherClassForBlocksWithErrorInTimeInit)  # noqa
    with pytest.raises(OrchServError):
        block_s.set_next(OtherClassForBlocksWithErrorInTimeInitWithoutArguments)  # noqa
    block_f.set_next(block_s)
    assert block_f.get_list_flow() == "first async block -> second async block -> end"
    await block_f.handle(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))
    assert CONST_LIST_ASYNC == [1]
    await block_f.handle(deepcopy(MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK))
    assert CONST_LIST_ASYNC == [1, 2]

    block_f = FirstAsyncBlock(
        pre_handler_function=async_tst_method_with_correct_processing,
        post_handler_function=async_tst_method_with_correct_processing,
    )
    block_s = SecondAsyncBlock(
        pre_handler_function=async_tst_method_with_correct_processing,
        post_handler_function=async_tst_method_with_correct_processing,
    )
    block_f.set_next(block_s)

    await block_f.handle(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))
    assert CONST_LIST_ASYNC == [1, 2, -1, 1, -1]
    await block_f.handle(deepcopy(MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK))
    assert CONST_LIST_ASYNC == [1, 2, -1, 1, -1, -1, 2, -1]

    block_f = FirstAsyncBlock(
        pre_handler_function=async_tst_method_with_incorrect_processing,
        post_handler_function=async_tst_method_with_correct_processing,
    )
    block_s = SecondAsyncBlock(
        pre_handler_function=async_tst_method_with_incorrect_processing,
        post_handler_function=async_tst_method_with_correct_processing,
    )
    block_f.set_next(block_s)
    await block_f.handle(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))
    assert CONST_LIST_ASYNC == [1, 2, -1, 1, -1, -1, 2, -1, -2]
    await block_f.handle(deepcopy(MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK))
    assert CONST_LIST_ASYNC == [1, 2, -1, 1, -1, -1, 2, -1, -2, -2]

    assert block_f.get_next() == block_s
    assert block_s.get_next() is None

    CONST_LIST_ASYNC.clear()
    await block_f.process(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))
    assert CONST_LIST_ASYNC == [1]
    await block_s.process(deepcopy(MSG_TO_PROCESS_IN_FIRST_BLOCK))
    assert CONST_LIST_ASYNC == [1, 2]

    class TestClass(AsyncBaseBlock):
        pass

    class TestSecondClass(AsyncBaseBlock):
        async def set_next(self, handler: AsyncBaseBlock) -> AsyncBaseBlock:  # type: ignore  # noqa
            pass

        async def get_next(self) -> AsyncBaseBlock:  # type: ignore
            pass

        async def get_list_flow(self) -> str:  # type: ignore
            pass

        async def handle(self, message: BaseOrchServMsg) -> None:
            pass

        async def process(self, message: BaseOrchServMsg) -> Optional[BaseOrchServMsg]:
            pass

    with pytest.raises(TypeError):
        TestClass()
    with pytest.raises(NotImplementedError):
        TestSecondClass().name_block
    with pytest.raises(NotImplementedError):
        TestSecondClass().pre_handler_function
    with pytest.raises(NotImplementedError):
        TestSecondClass().post_handler_function

    async def test_funct(msg):
        pass

    block_f = FirstAsyncBlock()
    block_f.pre_handler_function = test_funct
    assert block_f.pre_handler_function == test_funct
    block_f.post_handler_function = test_funct
    assert block_f.post_handler_function == test_funct
    block_f = FirstAsyncBlock()

    block_f.pre_handler_function = ""
    block_f.post_handler_function = ""
    assert block_f.pre_handler_function is None
    assert block_f.post_handler_function is None

    with pytest.raises(TypeError):
        block_f.pre_handler_function = 1
    with pytest.raises(TypeError):
        block_f.pre_handler_function = "sad"
    with pytest.raises(TypeError):
        block_f.post_handler_function = 1
    with pytest.raises(TypeError):
        block_f.post_handler_function = "sad"
