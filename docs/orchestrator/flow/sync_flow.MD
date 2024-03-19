# Module `sync_flow.py`
```text
Flow for sync mode
```

> Path: `orch_serv/orchestrator/flow/sync_flow.py`
## Class `SyncFlow`
```text
SyncFlow for execution SyncBlock
```

### Basses(s)
+ Flow
+ ABC
### SubElement(s)
 > `_base_class_for_blocks` = SyncBlock
 > `flow_chain`: SyncBlock = None
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