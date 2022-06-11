"""
Example setup and use orchestrator
"""
import asyncio
from typing import Optional

from example_blocks import (
    FirstAsyncBlock,
    FirstBlock,
    SecondAsyncBlock,
    SecondBlock,
    importer_async_block,
    importer_sync_block,
)
from example_flows import (
    FirstAsyncFlow,
    FirstFlow,
    SecondAsyncFlow,
    SecondFlow,
    importer_async_flows,
    importer_sync_flows,
)
from pydantic import BaseModel

from orch_serv import AsyncOrchestrator, BaseOrchServMsg, Orchestrator


class BodyModel(BaseModel):
    body_option: Optional[str]


class HeaderModel(BaseModel):
    source: Optional[str]
    flow: Optional[str]
    target: Optional[str]


class ExampleMessageModel(BaseOrchServMsg):
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


orchestrator1 = Orchestrator(flows=importer_sync_flows, blocks=importer_sync_block)
orchestrator2 = Orchestrator(
    flows=[FirstFlow, SecondFlow],
    blocks=[FirstBlock, SecondBlock],
    default_flow=FirstFlow.name_flow,
    default_block=FirstBlock.name_block,
    flows_to_ignore=[SecondFlow.__name__],
    blocks_to_ignore=[SecondBlock.__name__],
)


class ExampleOrchestrator(Orchestrator):
    flows = [FirstFlow, SecondFlow]
    blocks = [FirstBlock, SecondBlock]


orchestrator3 = ExampleOrchestrator()
print("Flows orchestrator2", orchestrator2.get_list_flows())
print("Blocks orchestrator2", orchestrator2.get_list_blocks())
print("Blocks orchestrator3", orchestrator3.get_list_blocks())
# and mixed

async_orchestrator1 = AsyncOrchestrator(
    flows=importer_async_flows, blocks=importer_async_block
)
async_orchestrator2 = AsyncOrchestrator(
    flows=[FirstAsyncFlow, SecondAsyncFlow], blocks=[FirstAsyncBlock, SecondAsyncBlock]
)
print("Flows async_orchestrator2", async_orchestrator2.get_list_flows())
print("Blocks async_orchestrator2", async_orchestrator2.get_list_blocks())


# and mixed


def main():
    print("Orchestrator")

    msg = ExampleMessageModel(body=dict(), header=dict(flow="first_flow"))
    result = orchestrator2.handle(msg)
    print("Default handler", result)
    result = orchestrator2.handle(msg, is_force_return=True)
    print("NotDefault handler", result)


async def async_main():
    print("AsyncOrchestrator")
    msg = ExampleMessageModel(body=dict(), header=dict(flow="first_async_flow"))
    result = await async_orchestrator2.handle(msg)
    print("Default handler", result)
    result = await async_orchestrator2.handle(msg, is_force_return=True)
    print("NotDefault handler", result)


if __name__ == "__main__":
    main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
    loop.close()
