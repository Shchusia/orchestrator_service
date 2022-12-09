# Module `sync_block.py`
```text
Module with base block class for user sync blocks
```

> Path: `orch_serv\orchestrator\block\sync_block.py`
## Class `SyncBlock`
```text
Base block for sync mode
```

### Basses(s)
+ SyncBaseBlock
+ ABC
### Attributes(s)
+ _next_handler`:SyncBaseBlock - the object of the next handler
in the flow where this block participates
+ _pre_handler_function`:Optional[
Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]
] - function called before this block's handler
+ _post_handler_function`:Optional[
Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]
] - function called after this block's handler
### SubElement(s)
 > `_next_handler`: SyncBaseBlock = None
 > `_pre_handler_function`: Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]] = None
 > `_post_handler_function`: Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]] = None
 > ## Function  `is_execute_after_nullable_process_msg`
 > ```text
 > Execute if the block handler did not return a message
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ### Return
 > ```text
 > true if it should be executed with previous msg after empty process msg
 > ```
 > 
 > #### Declared returns: `bool`
 > ## Function  `pre_handler_function`
 > ```text
 > A class property that returns an synchronous function that will be
 > called before being sent to the main handler.
 > the function should only take one parameter msg: BaseOrchServMsg
 > Attention!!!
 > The function must return a message object.
 > If the function does not return a message, then the handler will not be called
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ### Return
 > ```text
 > sync function if exist pre_handler_function
 > ```
 > 
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]`
 > ## Function  `post_handler_function`
 > ```text
 > A class property that returns an synchronous function that will be
 > called after this block`s handler.
 > the function should only take one parameter msg: BaseOrchServMsg
 > if the `process` does not return a message to the function,
 > the message sent to the handler will be transferred
 > if it is not mandatory to execute, redefine
 > the variable `is_execute_after_nullable_process_msg = False` in your block
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ### Return
 > ```text
 > sync function if exist pre_handler_function
 > ```
 > 
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]`
 > ## Function  `pre_handler_function`
 > ```text
 > Method check pre_handler_function is func
 > ```
 > 
 > ### Decorator(s)
 > + pre_handler_function.setter
 > ### Argument(s)
 > + `func`: Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]] - object to check
 > ### Return
 > ```text
 > nothing
 > ```
 > 
 > ## Function  `post_handler_function`
 > ```text
 > Method check post_handler_function is func
 > ```
 > 
 > ### Decorator(s)
 > + post_handler_function.setter
 > ### Argument(s)
 > + `func`: Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]] - object to check
 > ### Return
 > ```text
 > nothing
 > ```
 > 
 > ## Function  `__init__`
 > ```text
 > Init Block
 > ```
 > 
 > ### Argument(s)
 > + `pre_handler_function`: Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]] - function should accept
 > and return objects of type Message
 > which be run before call method
 > + `post_handler_function`: Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]] - function should accept
 > and return objects of type Message
 > which be run after got msg from source
 > + `logger`: Optional[Logger] - orchestrator logger
 > ## Function  `set_next`
 > ```text
 > Save next handler after this handler in flow
 > ```
 > 
 > ### Argument(s)
 > + `handler`: Union[SyncBaseBlock, Type[SyncBaseBlock]] - empty doc string
 > ### Return
 > ```text
 > SyncBaseBlock
 > :raise Exception: some exception if error in time init handler if
 > handler provided as type
 > :raise TypeError: if handler not is instance of type SyncBaseBlock
 > ```
 > 
 > #### Declared returns: `SyncBaseBlock`
 > ## Function  `get_next`
 > ```text
 > the method returns the next block
 > ```
 > 
 > ### Return
 > ```text
 > next block if exist
 > ```
 > 
 > #### Declared returns: `Optional[SyncBaseBlock]`
 > ## Function  `_process_logic`
 > ```text
 > Auxiliary function in which the logic of working with additional
 > functions is hidden
 > ```
 > 
 > ### Argument(s)
 > + `block`: SyncBaseBlock - block for processing
 > + `message`: BaseOrchServMsg - message for processing
 > ### Return
 > ```text
 > nothing
 > ```
 > 
 > ## Function  `handle`
 > ```text
 > A function that determines which handler should now process
 > the message based on the source from which the message came.
 > ```
 > 
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - message for processing
 > ### Return
 > ```text
 > nothing
 > :raise FlowException: exception if a message with the wrong source
 > is passed to the flow
 > ```
 > 
 > ## Function  `get_list_flow`
 > ```text
 > Method return str flow
 > ```
 > 
 > ### Return
 > ```text
 > str
 > ```
 > 
 > #### Declared returns: `str`