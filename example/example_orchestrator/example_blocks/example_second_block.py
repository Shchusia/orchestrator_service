from orch_serv import BaseOrchServMsg
from orch_serv.orchestrator import AsyncBlock, SyncBlock


class SecondBlock(SyncBlock):
    name_block = "second block"

    def process(self, message: BaseOrchServMsg):
        # do something
        pass


class SecondAsyncBlock(AsyncBlock):
    name_block = "second async block"

    async def process(self, message: BaseOrchServMsg):
        # do something
        pass
