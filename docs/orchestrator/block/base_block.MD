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
 > The function that will be executed before the main handler
 > must return a message if the message is not returned,
 > then the message will not get into the handler
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]`
 > ## Function  `post_handler_function`
 > ```text
 > function to be executed after the main handler
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
 > Save Next handler after this handler in flow
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `handler`: SyncBaseBlock - empty doc string
 > ### Return
 > ```text
 > AsyncBaseBlock
 > :raise Exception: some exception if error is in time init handler if
 > handler provided as type
 > :raise TypeError: if handler is not instance of type SyncBaseBlock
 > ```
 > 
 > #### Declared returns: `SyncBaseBlock`
 > ## Function  `get_next`
 > ```text
 > the method returns the next block after
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Return
 > ```text
 > next block if exist
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
 > A function that determines which handler should now process
 > the message based on the source from which the message came.
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - message for processing
 > ### Return
 > ```text
 > nothing
 > :raise FlowException: exception if a message with the wrong source
 > is passed to the flow
 > ```
 > 
 > ## Function  `process`
 > ```text
 > Function to be redefined in subclasses which contains
 > the main logic of this block
 > If necessary, after executing this function, execute
 > the post function method that must return a message
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - message to process
 > ### Return
 > ```text
 > message after processing
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
 > The function that will be executed before the main handler.
 > Must return a message, if the message is not returned,
 > then the message will not get into the handler
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]]`
 > ## Function  `post_handler_function`
 > ```text
 > function to be executed after the main handler
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]]`
 > ## Function  `name_block`
 > ```text
 > Unique name to identify block
 > to override in subclass name_block
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ## Function  `set_next`
 > ```text
 > Save next handler after this handler in flow
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `handler`: AsyncBaseBlock - empty doc string
 > ### Return
 > ```text
 > AsyncBaseBlock
 > :raise Exception: some exception if error in time init handler if
 > handler provided as type
 > :raise TypeError: if handler not is instance of type SyncBaseBlock
 > ```
 > 
 > #### Declared returns: `AsyncBaseBlock`
 > ## Function  `get_next`
 > ```text
 > the method returns the next block after
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Return
 > ```text
 > next block if exist
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
 > A function that determines which handler should now process
 > the message based on the source from which the message came.
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - message for processing
 > ### Return
 > ```text
 > nothing
 > :raise FlowException: exception if a message with the wrong source
 > is passed to the flow
 > ```
 > 
 > ## Function `async` `process`
 > ```text
 > Function to be redefined in subclasses which contains
 > the main logic of this block
 > If necessary, after executing this function, execute
 > the post function method must return a message
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - message to process
 > ### Return
 > ```text
 > message after processing
 > ```
 > 
 > #### Declared returns: `Optional[BaseOrchServMsg]`