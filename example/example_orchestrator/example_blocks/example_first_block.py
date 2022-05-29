from orch_serv import BaseOrchServMsg
from orch_serv.orchestrator import AsyncBlock, SyncBlock


class FirstBlock(SyncBlock):
    name_block = "first block"

    def process(self, message: BaseOrchServMsg):
        # do something
        pass


class FirstAsyncBlock(AsyncBlock):
    name_block = "first async block"

    async def process(self, message: BaseOrchServMsg):
        # do something
        pass
