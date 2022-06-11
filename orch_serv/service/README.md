# orch_serv.service

> The module contains classes for creating a microservice. Able to perform different tasks.

## Service creation

#### Process logic
> Class with message processing logic for a given command

> There can be several such classes with different logic.
> The `target_command` must be unique

```python
from typing import Any, Tuple, Union

from orch_serv.service import CommandHandlerProcessStrategy
from orch_serv.msg import BaseOrchServMsg

class ExampleProcessStrategy(CommandHandlerProcessStrategy):
    target_command = "first_command"

    def process(
        self, msg: BaseOrchServMsg
    ) -> Union[Tuple[BaseOrchServMsg, Any], BaseOrchServMsg]:
        # do something
        return msg
```


#### PostProcess logic
> Class with post-processing logic

```python
from typing import Any, Optional

from orch_serv import (
    BaseOrchServMsg,
    CommandHandlerPostProcessStrategy,
)


class ExamplePostProcessHandler(CommandHandlerPostProcessStrategy):
    def post_process(self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None):
        # do something
        pass
```

#### Service setup
> service configuration

```python
from orch_serv.service import Service, ServiceBlock, ServiceBuilder
class ExampleService(Service):
    service_commands = ServiceBuilder(
        ServiceBlock(processor=ExampleProcessStrategy, post_processor=ExamplePostProcessHandler),
        default_post_process=ExamplePostProcessHandler,
    )
```

#### Use the service

```python
msg: BaseOrchServMsg
service = ExampleService()
service.handle(msg)
```

> Similarly for asynchronous Service

## Additionally
> commands can transfer data between themselves within the service

Example:
```python
class ExampleProcessStrategy(CommandHandlerProcessStrategy):
    target_command = "first_command"

    def process(
        self, msg: BaseOrchServMsg
    ) -> Union[Tuple[BaseOrchServMsg, Any], BaseOrchServMsg]:
        # do something
        return msg
```


