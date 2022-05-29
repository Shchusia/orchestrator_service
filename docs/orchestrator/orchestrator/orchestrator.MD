# Module `orchestrator.py`
```text
Module with sync orchestrator
```

> Path: `orch_serv\orchestrator\orchestrator\orchestrator.py`
## Class `Orchestrator`
```text
Orchestrator class for build service
```

### SubElement(s)
 > `_base_class_for_flow` = SyncFlow
 > `_base_class_for_target` = SyncBlock
 > `_default_flow`: str = None
 > `_default_block`: str = None
 > `_flows`: Dict[str, Union[Type[Union[SyncFlow, AsyncFlow]], Union[SyncFlow, AsyncFlow]]] = dict()
 > `_targets`: Dict[str, Union[Type[Union[SyncBlock, AsyncBlock]], Union[SyncBlock, AsyncBlock]]] = dict()
 > ## Function  `__init__`
 > ### Argument(s)
 > + `flows`: Optional[Union[ModuleType, List]] - empty doc string
 > + `blocks`: Optional[Union[ModuleType, List]] - empty doc string
 > + `logger`: Optional[Logger] - empty doc string
 > + `flows_to_ignore`: List[str] - empty doc string
 > + `blocks_to_ignore`: List[str] - empty doc string
 > + `default_flow`: Optional[str] - empty doc string
 > + `default_block`: Optional[str] - empty doc string
 > ## Function  `get_list_flows`
 > ```text
 > return list allowed flows
 > ```
 > 
 > #### Declared returns: `List[str]`
 > ## Function  `get_list_blocks`
 > ```text
 > return list allowed blocks
 > ```
 > 
 > #### Declared returns: `List[str]`
 > ## Function  `_validate_data`
 > ```text
 > Checks the types of objects in the flow and goals so that
 > the synchronous orchestrator does not redistribute a
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
 > !!! the presence of a `target` in the message is more priority
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