from typing import Optional

from pydantic import BaseModel

from orch_serv import AsyncBlock, BaseOrchServMsg, SyncBlock


class BodyModel(BaseModel):
    body_option: Optional[str]


class HeaderModel(BaseModel):
    source: Optional[str]


class MyTestModel(BaseOrchServMsg):
    body: BodyModel
    header: HeaderModel

    def get_source(self):
        return self.header.source

    def set_source(self, source: str):
        self.header.source = source


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


class FirstAsyncBlock(AsyncBlock):
    name_block = "first async block"

    async def process(self, msg: BaseOrchServMsg):
        CONST_LIST_ASYNC.append(1)


class SecondAsyncBlock(AsyncBlock):
    name_block = "second async block"

    async def process(self, msg: BaseOrchServMsg):
        CONST_LIST_ASYNC.append(2)


MSG_TO_PROCESS_IN_FIRST_BLOCK = MyTestModel(body=dict(), header=dict())
MSG_TO_PROCESS_IN_SECOND_BLOCK = MyTestModel(
    body=dict(), header=dict(source="first block")
)
MSG_TO_PROCESS_IN_SECOND_ASYNC_BLOCK = MyTestModel(
    body=dict(), header=dict(source="first async block")
)


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
