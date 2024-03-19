# Module `async_flow.py`
```text
Flow for sync mode
```

> Path: `orch_serv/orchestrator/flow/async_flow.py`
## Class `AsyncFlow`
```text
AsyncFlow for execution async blocks
```

### Basses(s)
+ Flow
+ ABC
### SubElement(s)
 > `_base_class_for_blocks` = AsyncBlock
 > `flow_chain`: AsyncBlock = None
 > ## Function `async` `to_go_with_the_flow`
 > ```text
 > Method that starts flow execution from the first block
 > ```
 > 
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - message to process
 > ### Return
 > ```text
 > None
 > ```
 > 