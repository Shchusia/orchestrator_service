# Module `exc.py`
```text
Module consolidate all exceptions lib
```

> Path: `orch_serv\exc.py`
## Class `OrchServError`
```text
Main exception class for custom exception lib
```

### Basses(s)
+ Exception
## Class `MsgException`
```text
Main exception class for exceptions with msg
```

### Basses(s)
+ OrchServError
## Class `OrchestratorException`
```text
Main exception class exceptions with Orchestrator
```

### Basses(s)
+ OrchServError
## Class `FlowException`
```text
Error if the handler for the current message
is not found in the flow
```

### Basses(s)
+ OrchestratorException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `message`: str - empty doc string
## Class `FlowBlockException`
```text
Class custom exception
for wrong type of flow block
```

### Basses(s)
+ OrchestratorException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `message`: str - empty doc string
## Class `FlowBuilderException`
```text
Class custom exception
for wrong types
```

### Basses(s)
+ OrchestratorException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `message`: str - empty doc string
## Class `UniqueNameException`
```text
Exception for not unique flows
```

### Basses(s)
+ OrchestratorException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `not_unique_flow_name`: str - empty doc string
 > + `_type`: str - empty doc string
## Class `NoDateException`
```text
Exception if dict flow is empty
```

### Basses(s)
+ OrchestratorException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `_type` - empty doc string
 > + `msg`: Optional[str] - empty doc string
## Class `WrongTypeException`
```text
Exception for incorrect inputted types
```

### Basses(s)
+ OrchestratorException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `variable`: str - empty doc string
 > + `type_variable`: str - empty doc string
## Class `WorkTypeMismatchException`
```text
if an asynchronous class is used for
a synchronous orchestra, or vice versa
```

### Basses(s)
+ OrchestratorException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `base_class`: str - empty doc string
 > + `obj_class`: str - empty doc string
 > + `is_target`: bool - empty doc string
## Class `NotFoundDefaultError`
```text
If provided default value but default value not exist in processed data
```

### Basses(s)
+ OrchestratorException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `default_value`: str - empty doc string
 > + `allowed_values`: List[str] - empty doc string
 > + `is_target`: bool - empty doc string