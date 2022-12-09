# Module `sync_orchestrator.py`
```text
Module with sync orchestrator
```

> Path: `orch_serv\orchestrator\orchestrator\sync_orchestrator.py`
## Class `SyncOrchestrator`
```text
Orchestrator class for build service
```

### SubElement(s)
 > `_base_class_for_flow`: Type[Union[SyncFlow, AsyncFlow]] = SyncFlow
 > `_base_class_for_target`: Type[Union[SyncBlock, AsyncBlock]] = SyncBlock
 > `_default_flow`: str = None
 > `_default_block`: str = None
 > `_flows`: Dict[str, Union[Type[Union[SyncFlow, AsyncFlow]], Union[SyncFlow, AsyncFlow]]] = dict()
 > `_targets`: Dict[str, Union[Type[Union[SyncBlock, AsyncBlock]], Union[SyncBlock, AsyncBlock]]] = dict()
 > ## Function  `flows`
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Union[ModuleType, List]]`
 > ## Function  `blocks`
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Union[ModuleType, List]]`
 > ## Function  `__init__`
 > ```text
 > init Orchestrator
 > ```
 > 
 > ### Argument(s)
 > + `flows`: Optional[Union[ModuleType, List]] - data flows to init for current orchestrator
 > + `blocks`: Optional[Union[ModuleType, List]] - data blocks to init for current orchestrator
 > + `logger`: Optional[Logger] - logger orchestrator
 > + `flows_to_ignore`: List[str] - name of the flows to
 > ignore which will not be initialized
 > + `blocks_to_ignore`: List[str] - name of the blocks to
 > ignore which will not be initialized
 > + `default_flow`: Optional[str] - name of the flow that will be called
 > if a non-existing flow is specified
 > + `default_block`: Optional[str] - name of the block that will be called
 > if a non-existing block is specified
 > ## Function  `get_list_flows`
 > ### Return
 > ```text
 > list allowed flows
 > ```
 > 
 > #### Declared returns: `List[str]`
 > ## Function  `get_list_blocks`
 > ### Return
 > ```text
 > list allowed blocks
 > ```
 > 
 > #### Declared returns: `List[str]`
 > ## Function  `_validate_data`
 > ```text
 > Checks the types of objects in the flow and targets the
 > synchronous orchestrator not to redistribute a
 > synchronous flows or blocks and vice versa
 > :raise WorkTypeMismatchException: if incorrect type
 > ```
 > 
 > ### SubElement(s)
 > > ## Function  `get_name`
 > > ### Argument(s)
 > > + `obj` - empty doc string
 > > #### Declared returns: `str`
 > > ## Function  `check_type_dict_obj`
 > > ### Argument(s)
 > > + `dict_objects`: Dict[str, Any] - empty doc string
 > > + `type_to_check`: Type - empty doc string
 > > + `is_target`: bool - empty doc string
 > ## Function  `_generate_data`
 > ```text
 > The method prepares the data for the orchestrator to work
 > Converts data from a list or retrieves from a module
 > ```
 > 
 > ### Decorator(s)
 > + staticmethod
 > ### Argument(s)
 > + `data_to_process`: Union[ModuleType, List] - empty doc string
 > + `type_to_compare`: Union[Type, Tuple[Type, ...]] - empty doc string
 > + `attribute_to_get`: str - name in object
 > + `names_to_ignore`: Optional[List[str]] - class names to ignore when processing
 > + `type_data`: str - name for information exception if will be raised
 > ### Return
 > ```text
 > converted data to dictionary format to work with
 > ```
 > 
 > #### Declared returns: `Dict[str, Type[Union[SyncFlow, AsyncFlow, SyncBlock, AsyncBlock]]]`
 > ## Function  `handle`
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