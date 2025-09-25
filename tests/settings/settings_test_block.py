from typing import Any, Optional

from pydantic import BaseModel

from orch_serv import AsyncBlock, BaseOrchServMsg, SyncBlock
from orch_serv.exc import OrchServError


class BodyModel(BaseModel):
    body_option: Optional[str]= None


class HeaderModel(BaseModel):
    source: Optional[str]= None
    flow: Optional[str]= None
    target: Optional[str] = None


class MyTestModel(BaseOrchServMsg):
    body: BodyModel
    header: HeaderModel

    def get_source(self):
        return self.header.source

    def set_source(self, source: str):
        self.header.source = source

    def get_target(self):
        return self.header.target

    def get_flow(self):
        return self.header.flow


CONST_LIST_SYNC = []
CONST_LIST_ASYNC = []


class FirstBlock(SyncBlock):
    name_block = "first block"

    def process(self, msg: BaseOrchServMsg):
        CONST_LIST_SYNC.append(1)


class SecondBlock(SyncBlock):
    name_block = "second block"

    def process(self, msg: BaseOrchServMsg):
        CONST_LIST_SYNC.append(2)
        return msg


class ThirdBlock(SyncBlock):
    name_block = "third block"
    is_execute_after_nullable_process_msg = True

    def process(self, msg: BaseOrchServMsg):
        CONST_LIST_SYNC.append(3)
        return None


class FourthBlock(SyncBlock):
    name_block = "fourth block"
    is_execute_after_nullable_process_msg = False

    def process(self, msg: BaseOrchServMsg):
        CONST_LIST_SYNC.append(4)
        return None


class FifthBlock(SyncBlock):
    name_block = "fifth block"
    is_execute_after_nullable_process_msg = False

    def process(self, msg: BaseOrchServMsg):
        raise Exception


class FirstAsyncBlock(AsyncBlock):
    name_block = "first async block"

    async def process(self, msg: BaseOrchServMsg):
        CONST_LIST_ASYNC.append(1)


class SecondAsyncBlock(AsyncBlock):
    name_block = "second async block"

    async def process(self, msg: BaseOrchServMsg):
        CONST_LIST_ASYNC.append(2)
        return msg


class ThirdAsyncBlock(AsyncBlock):
    name_block = "third async block"
    is_execute_after_nullable_process_msg = True

    async def process(self, msg: BaseOrchServMsg):
        CONST_LIST_ASYNC.append(3)
        return None


class FourthAsyncBlock(AsyncBlock):
    name_block = "fourth async block"
    is_execute_after_nullable_process_msg = False

    async def process(self, msg: BaseOrchServMsg):
        CONST_LIST_ASYNC.append(4)
        return None


class FifthAsyncBlock(AsyncBlock):
    name_block = "fifth async block"
    is_execute_after_nullable_process_msg = False

    async def process(self, msg: BaseOrchServMsg):
        raise Exception


MSG_TO_PROCESS_IN_FIRST_BLOCK = MyTestModel(body=dict(), header=dict())
MSG_TO_PROCESS_IN_SECOND_BLOCK = MyTestModel(
    body=dict(), header=dict(source="first block")
)
MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK = MyTestModel(
    body=dict(), header=dict(source="first async block")
)
MSG_TO_PROCESS_IN_THIRD_ASYNC_BLOCK = MyTestModel(body=dict(), header=dict())
MSG_TO_PROCESS_IN_FORTH_ASYNC_BLOCK = MyTestModel(body=dict(), header=dict())
MSG_TO_PROCESS_IN_THIRD_SYNC_BLOCK = MyTestModel(body=dict(), header=dict())
MSG_TO_PROCESS_IN_FORTH_SYNC_BLOCK = MyTestModel(body=dict(), header=dict())


def tst_method_with_correct_processing(msg: BaseOrchServMsg) -> BaseOrchServMsg:
    CONST_LIST_SYNC.append(-1)
    return msg


def tst_method_with_incorrect_processing(msg: BaseOrchServMsg) -> None:
    CONST_LIST_SYNC.append(-2)
    return None


async def async_tst_method_with_correct_processing(msg: BaseOrchServMsg):
    CONST_LIST_ASYNC.append(-1)
    return msg


async def async_tst_method_with_incorrect_processing(msg: BaseOrchServMsg):
    CONST_LIST_ASYNC.append(-2)
    return None


class OtherClassForBlocks:
    pass


class OtherClassForBlocksWithErrorInTimeInit:
    def __init__(self, some_argument: Any):
        self.some_argument = some_argument


class OtherClassForBlocksWithErrorInTimeInitWithoutArguments:
    def __init__(self):
        raise OrchServError
