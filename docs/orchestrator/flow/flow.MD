# Module `flow.py`
```text
Flow for sync mode
```

> Path: `orch_serv\orchestrator\flow\flow.py`
## Class `SyncFlow`
```text
SyncFlow for execution SyncBlock
```

### Basses(s)
+ Flow
+ ABC
### SubElement(s)
 > `_base_class_for_blocks` = SyncBlock
 > `flow_chain`: Union[SyncBlock] = None
 > ## Function  `to_go_with_the_flow`
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