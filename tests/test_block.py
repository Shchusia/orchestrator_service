"""
Tests for block
"""
from copy import deepcopy

import pytest

from tests.settings.settings_test_block import (
    CONST_LIST_ASYNC,
    CONST_LIST_SYNC,
    MSG_TO_PROCESS_IN_FIRST_BLOCK,
    MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK,
    MSG_TO_PROCESS_IN_SECOND_BLOCK,
    FirstAsyncBlock,
    FirstBlock,
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
        block = block_f.set_next(FirstAsyncBlock())  # noqa
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


@pytest.mark.asyncio
async def test_async_block():
    block_f = FirstAsyncBlock()
    block_s = SecondAsyncBlock()

    with pytest.raises(TypeError):
        block = block_f.set_next(FirstBlock())  # noqa
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
