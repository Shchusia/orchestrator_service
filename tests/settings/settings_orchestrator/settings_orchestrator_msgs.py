from ..settings_test_block import MyTestModel

CORRECT_MSG_FIRST_FLOW_FIRST_BLOCK = MyTestModel(
    body=dict(), header=dict(flow="test_flow")
)
CORRECT_MSG_FIRST_FLOW_SECOND_BLOCK = MyTestModel(
    body=dict(), header=dict(flow="test_flow", source="first block")
)

CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK = MyTestModel(
    body=dict(), header=dict(flow="second_test_flow")
)
CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK = MyTestModel(
    body=dict(), header=dict(flow="second_test_flow", source="first block")
)
INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK = MyTestModel(
    body=dict(), header=dict(flow="second_test_flowsss", source="first block")
)
INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK2 = MyTestModel(
    body=dict(), header=dict(flow="second_test_flow", source="first blockssss")
)

CORRECT_MSG_TO_FIRST_BLOCK = MyTestModel(body=dict(), header=dict(target="first block"))
CORRECT_MSG_TO_SECOND_BLOCK = MyTestModel(
    body=dict(), header=dict(target="second block")
)
INCORRECT_MSG_TO_BLOCK = MyTestModel(
    body=dict(), header=dict(target="second blocksafa")
)
INCORRECT_MSG_TO_NotExistedBLOCK = MyTestModel(
    body=dict(), header=dict(target="test block")
)
CORRECT_MSG_TO_BLOCK_WITH_EXCEPTION = MyTestModel(
    body=dict(), header=dict(target="fifth block")
)
CORRECT_EMPTY_MSG = MyTestModel(body=dict(), header=dict())
CORRECT_MSG_TO_ASYNC_BLOCK_WITH_EXCEPTION = MyTestModel(
    body=dict(), header=dict(target="fifth async block")
)


ASYNC_CORRECT_MSG_FIRST_FLOW_FIRST_BLOCK = MyTestModel(
    body=dict(), header=dict(flow="test_async_flow")
)
ASYNC_CORRECT_MSG_FIRST_FLOW_SECOND_BLOCK = MyTestModel(
    body=dict(), header=dict(flow="test_async_flow", source="first async block")
)

ASYNC_CORRECT_MSG_SECOND_FLOW_FIRST_BLOCK = MyTestModel(
    body=dict(), header=dict(flow="second_test_async_flow")
)
ASYNC_CORRECT_MSG_SECOND_FLOW_SECOND_BLOCK = MyTestModel(
    body=dict(), header=dict(flow="second_test_async_flow", source="first async block")
)
ASYNC_INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK = MyTestModel(
    body=dict(),
    header=dict(flow="second_test_async_flowssss", source="first async block"),
)
ASYNC_INCORRECT_MSG_SECOND_FLOW_SECOND_BLOCK2 = MyTestModel(
    body=dict(),
    header=dict(flow="second_test_async_flow", source="first async blockssssss"),
)

ASYNC_CORRECT_MSG_TO_FIRST_BLOCK = MyTestModel(
    body=dict(), header=dict(target="first async block")
)
ASYNC_CORRECT_MSG_TO_SECOND_BLOCK = MyTestModel(
    body=dict(), header=dict(target="second async block")
)
ASYNC_INCORRECT_MSG_TO_BLOCK = MyTestModel(
    body=dict(), header=dict(target="second async blocksss")
)
