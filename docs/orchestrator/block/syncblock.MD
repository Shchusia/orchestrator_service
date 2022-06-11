# Module `syncblock.py`
```text
Sync Block
```

> Path: `orch_serv\orchestrator\block\syncblock.py`
## Class `SyncBlock`
```text
The main class for inheriting the blocks that make up the flow of tasks execution
```

### Basses(s)
+ SyncBaseBlock
+ ABC
### SubElement(s)
 > `_next_handler`: SyncBaseBlock = None
 > `_pre_handler_function`: Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]] = None
 > `_post_handler_function`: Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]] = None
 > ## Function  `pre_handler_function`
 > ```text
 > function which call before send to handler
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Optional[Callable[[BaseOrchServMsg], Optional[BaseOrchServMsg]]]`
 > ## Function  `post_handler_function`
 > ```text
 > function which call after received from source
 > ```
 > 
 > ### Decorator(s)
 > + property
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
 > Save Next handler after this handler
 > ```
 > 
 > ### Argument(s)
 > + `handler`: SyncBaseBlock - empty doc string
 > ### Return
 > ```text
 > Optional[BlockHandler, None]
 > ```
 > 
 > #### Declared returns: `SyncBaseBlock`
 > ## Function  `get_next`
 > #### Declared returns: `Optional[SyncBaseBlock]`
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
 > ## Function  `_process_logic`
 > ### Decorator(s)
 > + staticmethod
 > ### Argument(s)
 > + `block`: SyncBaseBlock - empty doc string
 > + `message`: BaseOrchServMsg - empty doc string
 > ## Function  `handle`
 > ```text
 > Method handle process msg
 > ```
 > 
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - msg to process
 > :raise FlowException: if not found handle for source from message
 > ### Return
 > ```text
 > nothing
 > ```
 > 