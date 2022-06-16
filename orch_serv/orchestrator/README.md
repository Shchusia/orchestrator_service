# orch_serv.orchestrator

> The module contains classes for creating an orchestrator

## Service creation

#### Create block 
> service image - knows how to send a message so that the microservice to which it is attached receives and processes it

```python
from orch_serv import BaseOrchServMsg
from orch_serv.orchestrator import AsyncBlock, SyncBlock


class ExampleBlock(SyncBlock):
    name_block = "example_block"

    def process(self, message: BaseOrchServMsg):
        # do something
        pass
```

#### Create flow 
> A chain of blocks connected by one processing goal is actually one task

```python
from typing import Optional

from orch_serv import BaseOrchServMsg
from orch_serv.orchestrator import FlowBlock, FlowBuilder, SyncFlow

def other_method(message: BaseOrchServMsg) -> Optional[BaseOrchServMsg]:
    # do something
    pass


class ExampleFlow(SyncFlow):
    name_flow = "ExampleFlow"
    steps_flow = FlowBuilder(
        FlowBlock(
            ExampleBlock,
            pre_handler_function="static_flow_method",
            post_handler_function=other_method,
        ),
    )

    @staticmethod
    def static_flow_method(message: BaseOrchServMsg) -> Optional[BaseOrchServMsg]:
        # do something
        pass
``` 

#### Create Orchestrator

```python
from orch_serv import SyncOrchestrator


class ExampleOrchestrator(SyncOrchestrator):
    flows = [ExampleFlow]
    blocks = [ExampleBlock]
```

#### Use orchestrator

```python
from orch_serv import SyncOrchestrator

msg: BaseOrchServMsg
orchestrator = ExampleOrchestrator()
orchestrator_alternative = SyncOrchestrator(
    flows=[ExampleFlow],
    blocks=[ExampleBlock])
orchestrator.handle(msg)
```
### [MoreExamples](../../example/example_orchestrator/README.md)