# Module `service.py`
```text
Module Service with help classes for build service
```

> Path: `orch_serv/service/service.py`
## Class `CommandHandler`
```text
Class with method for all handlers
```

### Basses(s)
+ ABC
### SubElement(s)
 > `_logger`: Logger = DEFAULT_LOGGER
 > `_service_instance`: Service = None
 > `_is_logged` = False
 > ## Function  `logger`
 > ```text
 > get logger
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ### Return
 > ```text
 > logger or None
 > ```
 > 
 > #### Declared returns: `Optional[Logger]
 > `
 > ## Function  `set_logger`
 > ```text
 > Set logger to handler
 > ```
 > 
 > ### Argument(s)
 > + `val`: Any - logger
 > ### Return
 > ```text
 > nothing
 > :raise TypeError: if val is not a logger
 > ```
 > 
 > ## Function  `set_service_instance`
 > ```text
 > set to instance handler current service object for use swap
 > ```
 > 
 > ### Argument(s)
 > + `service`: Service - empty doc string
 > ### Return
 > ```text
 > nothing
 > ```
 > 
 > ## Function  `set_to_swap_scope`
 > ```text
 > Method adds a value to the global scope for access from all services
 > ```
 > 
 > ### Argument(s)
 > + `key`: str - name key
 > + `data`: Any - data to add
 > ### Return
 > ```text
 > bool: is_added_value
 > ```
 > 
 > #### Declared returns: `bool`
 > ## Function  `get_from_swap_scope`
 > ```text
 > Method gets a value available for all services from the global scope.
 > ```
 > 
 > ### Argument(s)
 > + `key`: str - name key to get value
 > ### Return
 > ```text
 > data if exist or None
 > ```
 > 
 > #### Declared returns: `Optional[Any]
 > `
 > ## Function  `del_from_swap_scope`
 > ```text
 > Method removes attribute from swap_scope if any
 > ```
 > 
 > ### Argument(s)
 > + `key`: str - empty doc string
 > #### Declared returns: `bool`
## Class `CommandHandlerProcessStrategy`
```text
Handler class for base processing message
```

### Basses(s)
+ CommandHandler
+ ABC
### SubElement(s)
 > ## Function  `target_command`
 > ```text
 > this command will determine that the message should be processed
 > by this particular service
 > must be unique within the service
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ## Function  `process`
 > ```text
 > the main method for executing the logic of this handler, must be overridden
 > in the inheritor
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `msg`: BaseOrchServMsg - msg from queue
 > ### Return
 > ```text
 > MessageQueue or None if return None post handler will not be called
 > ```
 > 
 > #### Declared returns: `Union[(Tuple[(BaseOrchServMsg, Any)], BaseOrchServMsg)]
 > `
## Class `CommandHandlerPostProcessStrategy`
```text
Post Process Handler
```

### Basses(s)
+ CommandHandler
+ ABC
### SubElement(s)
 > ## Function  `post_process`
 > ```text
 > method for post-processing
 > e.g. sending to another queue
 > , must be overridden in the inheritor
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `msg`: BaseOrchServMsg - empty doc string
 > + `additional_data`: Optional[Any]
 > - optional data got from processing block
 > ### Return
 > ```text
 > None
 > ```
 > 
## Class `AsyncCommandHandlerProcessStrategy`
```text
Handler class for base processing message
```

### Basses(s)
+ CommandHandler
+ ABC
### SubElement(s)
 > ## Function  `target_command`
 > ```text
 > this command will determine that the message
 > should be processed by this particular service
 > must be unique within the service
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ## Function `async` `process`
 > ```text
 > the main method for this handler execution logic, must be overridden
 > in the inheritor
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `msg`: BaseOrchServMsg - msg from queue
 > ### Return
 > ```text
 > MessageQueue or None if return None post handler will not be called
 > ```
 > 
 > #### Declared returns: `Union[(Tuple[(BaseOrchServMsg, Any)], BaseOrchServMsg)]
 > `
## Class `AsyncCommandHandlerPostProcessStrategy`
```text
Post Process Handler
```

### Basses(s)
+ CommandHandler
+ ABC
### SubElement(s)
 > ## Function `async` `post_process`
 > ```text
 > method does post-processing
 > e.g. sending to another queue
 > , must be overridden in the inheritor
 > ```
 > 
 > ### Decorator(s)
 > + abstractmethod
 > ### Argument(s)
 > + `msg`: BaseOrchServMsg - empty doc string
 > + `additional_data`: Optional[Any]
 > - optional data got from processing block
 > ### Return
 > ```text
 > None
 > ```
 > 
## Class `DefaultPostProcessStrategy`
### Basses(s)
+ CommandHandlerPostProcessStrategy
### SubElement(s)
 > ## Function  `post_process`
 > ```text
 > default post process function for sync service
 > ```
 > 
 > ### Argument(s)
 > + `msg`: BaseOrchServMsg - msg received after processing
 > + `additional_data`: Optional[Any]
 > - empty doc string
 > ### Return
 > ```text
 > None
 > ```
 > 
## Class `AsyncDefaultPostProcessStrategy`
### Basses(s)
+ AsyncCommandHandlerPostProcessStrategy
### SubElement(s)
 > ## Function `async` `post_process`
 > ```text
 > default post process function for async service
 > ```
 > 
 > ### Argument(s)
 > + `msg`: BaseOrchServMsg - msg received after processing
 > + `additional_data`: Optional[Any]
 > - empty doc string
 > ### Return
 > ```text
 > None
 > ```
 > 
## Class `ServiceCommand`
```text
Structure class
```

### Basses(s)
+ BaseModel
### SubElement(s)
 > `processor`: Union[(CommandHandlerProcessStrategy, AsyncCommandHandlerProcessStrategy)]
 > = None
 > `post_processor`: Union[(CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy)]
 > = None
 > ## Class `Config`
 > ### SubElement(s)
 > > `arbitrary_types_allowed` = True
## Class `ServiceBlock`
```text
Class for build service - one Block with process
and post process handlers
```

### SubElement(s)
 > `_processor`: Union[(CommandHandlerProcessStrategy, AsyncCommandHandlerProcessStrategy)]
 > = None
 > `_post_processor`: Optional[Union[(CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy)]]
 > = None
 > ## Function  `processor`
 > ```text
 > Property contains process handler
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ### Return
 > ```text
 > process command instance
 > ```
 > 
 > #### Declared returns: `Union[(CommandHandlerProcessStrategy, AsyncCommandHandlerProcessStrategy)]
 > `
 > ## Function  `post_processor`
 > ```text
 > Property contains post_process handler
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ### Return
 > ```text
 > post_processor instance
 > ```
 > 
 > #### Declared returns: `Union[(CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy)]
 > `
 > ## Function  `processor`
 > ```text
 > Setups service processor and checks type
 > ```
 > 
 > ### Decorator(s)
 > + processor.setter
 > 
 > ### Argument(s)
 > + `processor`: Union[(CommandHandlerProcessStrategy, AsyncCommandHandlerProcessStrategy, Type[CommandHandlerProcessStrategy], Type[AsyncCommandHandlerProcessStrategy])]
 > - empty doc string
 > ## Function  `post_processor`
 > ```text
 > Setups service processor and checks type
 > ```
 > 
 > ### Decorator(s)
 > + post_processor.setter
 > 
 > ### Argument(s)
 > + `post_processor`: Optional[Union[(CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy, Type[CommandHandlerPostProcessStrategy], Type[AsyncCommandHandlerPostProcessStrategy])]]
 > - empty doc string
 > ## Function  `__init__`
 > ```text
 > Init ServiceBlock
 > ```
 > 
 > ### Argument(s)
 > + `processor`: Union[(Type[CommandHandlerProcessStrategy], CommandHandlerProcessStrategy, Type[AsyncCommandHandlerProcessStrategy], AsyncCommandHandlerProcessStrategy)]
 > - empty doc string
 > + `post_processor`: Union[(Type[CommandHandlerPostProcessStrategy], CommandHandlerPostProcessStrategy, Type[AsyncCommandHandlerPostProcessStrategy], AsyncCommandHandlerPostProcessStrategy)]
 > - empty doc string
## Class `ServiceBuilder`
```text
Class for aggregating service commands
```

### SubElement(s)
 > `_default_post_processor`: Union[(CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy)]
 > = None
 > ## Function  `default_post_processor`
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Union[(CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy)]
 > `
 > ## Function  `default_post_processor`
 > ```text
 > Setups service processor and checks correct type
 > ```
 > 
 > ### Decorator(s)
 > + default_post_processor.setter
 > 
 > ### Argument(s)
 > + `default_post_processor`: Union[(CommandHandlerPostProcessStrategy, Type[CommandHandlerPostProcessStrategy], AsyncCommandHandlerPostProcessStrategy, Type[AsyncCommandHandlerPostProcessStrategy])]
 > - empty doc string
 > ## Function  `check_is_post_processor`
 > ```text
 > Method checks if obj is post_processor
 > ```
 > 
 > ### Decorator(s)
 > + staticmethod
 > ### Argument(s)
 > + `obj`: Any - empty doc string
 > + `message_error`: str - empty doc string
 > ## Function  `__init__`
 > ### Argument(s)
 > + `default_post_process`: Optional[Union[(Type[CommandHandlerPostProcessStrategy], CommandHandlerPostProcessStrategy, Type[AsyncCommandHandlerPostProcessStrategy], AsyncCommandHandlerPostProcessStrategy)]]
 > - empty doc string
 > + *`args`: ServiceBlock - empty doc string
 > ## Function  `build`
 > ```text
 > Method builds all commands' current service.
 > ```
 > 
 > ### Argument(s)
 > + `service_instance`: Service - current service
 > + `logger`: Optional[Logger]
 > - logger
 > ### Return
 > ```text
 > {command_name: ServiceCommand} dict commands and proccess classes
 > ```
 > 
 > #### Declared returns: `Dict[(str, ServiceCommand)]
 > `
## Class `Service`
```text
Class Service for handle msg-s
```

### Basses(s)
+ ABC
### SubElement(s)
 > `_service_commands`: ServiceBuilder = None
 > `_dict_handlers`: Dict[(str, ServiceCommand)]
 > = dict()
 > `_default_command`: str = None
 > `_base_process_class` = CommandHandlerProcessStrategy
 > `_base_post_process_class` = CommandHandlerPostProcessStrategy
 > ## Function  `__init__`
 > ### Argument(s)
 > + `service_commands`: Optional[ServiceBuilder]
 > - empty doc string
 > + `default_command`: Optional[str]
 > - empty doc string
 > + `logger`: Optional[Logger]
 > - empty doc string
 > + `is_catch_exceptions`: bool - empty doc string
 > ## Function  `__validate_service_builder`
 > ```text
 > Help function for service_builder object validation
 > ```
 > 
 > ### Argument(s)
 > + `service_builder`: ServiceBuilder - empty doc string
 > ## Function  `service_commands`
 > ### Decorator(s)
 > + property
 > #### Declared returns: `ServiceBuilder`
 > ## Function  `service_commands`
 > ### Decorator(s)
 > + service_commands.setter
 > 
 > ### Argument(s)
 > + `service_builder`: ServiceBuilder - empty doc string
 > ## Function  `_validate_data`
 > ```text
 > Help function to validate data service
 > ```
 > 
 > ## Function  `_get_service_command`
 > ```text
 > Function for get command to handle received message
 > ```
 > 
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - received message
 > ### Return
 > ```text
 > handler if exist
 > ```
 > 
 > #### Declared returns: `Optional[ServiceCommand]
 > `
 > ## Function  `handle`
 > ```text
 > the main function to process received messages
 > ```
 > 
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - message to process
 > + `is_force_return`: bool - return msgs all time after execution
 > ### Return
 > ```text
 > not processed msgs or received msgs if is_force_return==True
 > ```
 > 
 > #### Declared returns: `Optional[BaseOrchServMsg]
 > `
## Class `AsyncService`
### Basses(s)
+ Service
+ ABC
### SubElement(s)
 > `_base_process_class` = AsyncCommandHandlerProcessStrategy
 > `_base_post_process_class` = AsyncCommandHandlerPostProcessStrategy
 > ## Function `async` `handle`
 > ### Argument(s)
 > + `message`: BaseOrchServMsg - empty doc string
 > + `is_force_return`: bool - empty doc string
 > #### Declared returns: `Optional[BaseOrchServMsg]
 > `