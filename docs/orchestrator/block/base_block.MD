# Module `base_block.py`
```text
Module with block class from which flow chains are formed
```

> Path: `orch_serv\orchestrator\block\base_block.py`
## Class `SyncBaseBlock`
```text
Base class for handling sync blocks
```

### Basses(s)
+ ABC
### SubElement(s)
 > ## Function  `pre_handler_function`
 > ```text
 > property for override in subclass
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]`
 > ## Function  `post_handler_function`
 > ```text
 > property for override in subclass
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]`
 > ## Function  `name_block`
 > ```text
 > Unique name to identify block
 > for override in subclass   name_block
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ## Function  `set_next`
 > ```text
 > method for adding a new handler
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `handler`: SyncBaseBlock - object next handler in chain flow
 > ### Return
 > ```text
 > BlockHandler
 > ```
 > 
 > #### Declared returns: `SyncBaseBlock`
 > ## Function  `get_next`
 > ```text
 > method for get next handler if exist
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Return
 > ```text
 > BlockHandler
 > ```
 > 
 > #### Declared returns: `SyncBaseBlock`
 > ## Function  `get_list_flow`
 > ```text
 > Method return str steps flow
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Return
 > ```text
 > str
 > ```
 > 
 > #### Declared returns: `str`
 > ## Function  `handle`
 > ```text
 > flow chain management method
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - empty doc string
 > ### Return
 > ```text
 > None
 > ```
 > 
 > ## Function  `process`
 > ```text
 > Method for executing the logic of a given block
 > in it, only send messages to other services
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - message to process
 > ### Return
 > ```text
 > message
 > ```
 > 
 > #### Declared returns: `Optional[BaseOrchServMsg]`
## Class `AsyncBaseBlock`
```text
Base class for handling async blocks
```

### Basses(s)
+ ABC
### SubElement(s)
 > ## Function  `pre_handler_function`
 > ```text
 > property for override in subclass
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]]`
 > ## Function  `post_handler_function`
 > ```text
 > property for override in subclass
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]]`
 > ## Function  `name_block`
 > ```text
 > Unique name to identify block
 > for override in subclass   name_block
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ## Function  `set_next`
 > ```text
 > method for adding a new handler
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `handler`: AsyncBaseBlock - object next handler in chain flow
 > ### Return
 > ```text
 > BlockHandler
 > ```
 > 
 > #### Declared returns: `AsyncBaseBlock`
 > ## Function  `get_next`
 > ```text
 > method for get next handler if exist
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Return
 > ```text
 > next block
 > ```
 > 
 > #### Declared returns: `Optional[AsyncBaseBlock]`
 > ## Function  `get_list_flow`
 > ```text
 > Method return str steps flow
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Return
 > ```text
 > str
 > ```
 > 
 > #### Declared returns: `str`
 > ## Function `async` `handle`
 > ```text
 > flow chain management method
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - empty doc string
 > ### Return
 > ```text
 > None
 > ```
 > 
 > ## Function `async` `process`
 > ```text
 > Method for executing the logic of a given block
 > in it, only send messages to other services
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - message to process
 > ### Return
 > ```text
 > message
 > ```
 > 
 > #### Declared returns: `Optional[BaseOrchServMsg]`