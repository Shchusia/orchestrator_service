# Module `async_orchestrator.py`
```text
Module with async orchestrator
```

> Path: `orch_serv\orchestrator\orchestrator\async_orchestrator.py`
## Class `AsyncOrchestrator`
```text
AsyncOrchestrator
override handle function for async mode
```

### Basses(s)
+ SyncOrchestrator
### SubElement(s)
 > `_base_class_for_flow` = AsyncFlow
 > `_base_class_for_target` = AsyncBlock
 > ## Function `async` `handle`
 > ```text
 > Message processing method
 > !!! the presence of a `target` in the message has higher priority
 > than the presence of a `flow`
 > ```
 > 
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - message to process
 > + `is_force_return`: bool - always return a message
 > ### Return
 > ```text
 > message if an error occurred while processing the message
 > if is_force_return is False
 > ```
 > 
 > #### Declared returns: `Optional[BaseOrchServMsg]`