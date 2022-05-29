# Module `async_block.py`
```text
module with base block class for user async blocks
```

> Path: `orch_serv\orchestrator\block\async_block.py`
## Class `AsyncBlock`
```text
Base block for async mode
```

### Basses(s)
+ AsyncBaseBlock
+ ABC
### SubElement(s)
 > `_next_handler`: AsyncBaseBlock = None
 > `_pre_handler_function`: Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]] = None
 > `_post_handler_function`: Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]] = None
 > ## Function  `pre_handler_function`
 > ```text
 > function which call before send to handler
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]]`
 > ## Function  `post_handler_function`
 > ```text
 > function which call after received from source
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]]`
 > ## Function  `pre_handler_function`
 > ```text
 > Method check pre_handler_function is func
 > ```
 > 
 > ### Decorator(s)
 > + pre_handler_function.setter
 > ### Argument(s)
 > + `func`: Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]] - object to check
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
 > + `func`: Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]] - object to check
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
 > + `pre_handler_function`: Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]] - function should accept
 > and return objects of type Message
 > which be run before call method
 > + `post_handler_function`: Optional[Callable[[BaseOrchServMsg], Awaitable[Optional[BaseOrchServMsg]]]] - function should accept
 > and return objects of type Message
 > which be run after got msg from source
 > + `logger`: Optional[Logger] - orchestrator logger
 > ## Function  `set_next`
 > ```text
 > Save Next handler after this handler
 > ```
 > 
 > ### Argument(s)
 > + `handler`: AsyncBaseBlock - empty doc string
 > ### Return
 > ```text
 > Optional[BlockHandler, None]
 > ```
 > 
 > #### Declared returns: `AsyncBaseBlock`
 > ## Function  `get_next`
 > #### Declared returns: `Optional[AsyncBaseBlock]`
 > ## Function `async` `process`
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - empty doc string
 > ## Function `async` `_process_logic`
 > ### Decorator(s)
 > + staticmethod
 > ### Argument(s)
 > + `block`: AsyncBaseBlock - empty doc string
 > + `message`: BaseOrchServMsg - empty doc string
 > ## Function `async` `handle`
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - empty doc string
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