# Module `base_flow.py`
```text
Module with classes for build flow
```

> Path: `orch_serv\orchestrator\flow\base_flow.py`
## Class `FlowBlock`
```text
Block for FlowBuilder
```

### SubElement(s)
 > `obj_block`: Union[SyncBlock, AsyncBlock, type] = None
 > ## Function  `__init__`
 > ```text
 > Init FlowBlock
 > ```
 > 
 > ### Argument(s)
 > + `obj_block`: Union[SyncBlock, AsyncBlock, Type[Union[SyncBlock, AsyncBlock]]] - block for flow
 > + `pre_handler_function`: Optional[Union[str, types.FunctionType, types.MethodType, Callable]] - optional function for execution before block
 > + `post_handler_function`: Optional[Union[str, types.FunctionType, types.MethodType, Callable]] - empty doc string
 > ## Function  `_get_function`
 > ```text
 > helper function that returns a function if specified for the block
 > ```
 > 
 > ### Decorator(s)
 > + staticmethod
 > ### Argument(s)
 > + `instance_main`: Flow - empty doc string
 > + `function_to_get`: Optional[Union[str, types.FunctionType, types.MethodType, Callable]] - name of function or the function itself
 > ### Return
 > ```text
 > a function object if provided
 > ```
 > 
 > #### Declared returns: `Optional[Union[types.FunctionType, types.MethodType, Callable]]`
 > ## Function  `init_block`
 > ```text
 > Method init instance subclass MainBlock
 > ```
 > 
 > ### Argument(s)
 > + `instance_main`: Flow - flow object for which this
 > block is initialized
 > + `step_number`: int - sequence number of the current block
 > ### Return
 > ```text
 > object subclass MainBlock
 > ```
 > 
 > #### Declared returns: `Union[SyncBlock, AsyncBlock]`
## Class `FlowBuilder`
```text
Flow building class
build chain flow from flow blocks
```

### SubElement(s)
 > ## Function  `__init__`
 > ```text
 > Init FlowBuilder
 > ```
 > 
 > ### Argument(s)
 > + `step`: FlowBlock - first block in flow
 > + *`args`: List[FlowBlock] - other steps  if value exist
 > ## Function  `build_flow`
 > ```text
 > Build chain flow for Flow
 > ```
 > 
 > ### Argument(s)
 > + `instance_main`: Flow - current flow
 > ### Return
 > ```text
 > the first block in the flow chain
 > ```
 > 
 > #### Declared returns: `Union[SyncBlock, AsyncBlock]`
## Class `Flow`
```text
Class for inheritance for a specific flow
```

### Attributes(s)
+ flow_chain`:Union[SyncBlock, AsyncBlock] - flow chain starting from the first block
+ is_contains_duplicat_blocks`:bool - whether the flow contains repeating blocks
needed to avoid looping
### SubElement(s)
 > `flow_chain`: Optional[Union[SyncBaseBlock, AsyncBaseBlock]] = None
 > `is_contains_duplicat_blocks`: bool = False
 > ## Function  `name_flow`
 > ```text
 > Unique name to identify flow
 > for override in subclass 'name_flow'
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ### Return
 > ```text
 > name flow
 > ```
 > 
 > #### Declared returns: `str`
 > ## Function  `_base_class_for_blocks`
 > ```text
 > An additional property for child classes to make the flow work only
 > with synchronous or asynchronous blocks.
 > necessary to maintain integrity
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Type[Union[AsyncBlock, SyncBlock]]`
 > ## Function  `steps_flow`
 > ```text
 > blocks that make up the current flow
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ## Function  `steps_flow`
 > ```text
 > check the set value to property `steps_flow` value
 > ```
 > 
 > ### Decorator(s)
 > + steps_flow.setter
 > ### Argument(s)
 > + `flow`: FlowBuilder - builder flow for current flow
 > ### Return
 > ```text
 > None or exception
 > ```
 > 
 > ## Function  `__init__`
 > ```text
 > Init Flow
 > ```
 > 
 > ### Argument(s)
 > + `logger`: Optional[Logger] - orchestrator logger
 > ## Function  `_validate_data`
 > ```text
 > flow validation function after initialization
 > ```
 > 
 > ## Function  `get_steps`
 > ```text
 > Print steps flow
 > ```
 > 
 > #### Declared returns: `str`