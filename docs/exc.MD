# Module `exc.py`
```text
Module consolidating all exceptions lib
```

> Path: `orch_serv/exc.py`
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
for incorrect type of flow block
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
 > + `msg`: Optional[str]
 > - empty doc string
## Class `WrongTypeException`
```text
Exception for incorrect input types
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
If provided default value but default value does not exist in processed data
```

### Basses(s)
+ OrchestratorException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `default_value`: str - empty doc string
 > + `allowed_values`: List[str]
 > - empty doc string
 > + `is_target`: bool - empty doc string
## Class `NotUniqueBlockInFlowError`
```text
If provided default value but default value does not exist in processed data
```

### Basses(s)
+ OrchestratorException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `block_name`: str - empty doc string
 > + `flow_name`: str - empty doc string
## Class `ServiceException`
```text
Main exception class exceptions with Service
```

### Basses(s)
+ OrchServError
## Class `ServiceBlockException`
```text
Class for exceptions in ServiceBlock
```

### Basses(s)
+ ServiceException
## Class `DoublePostProcessFunctionDeclaredError`
```text
Exception if many default postprocess handlers
```

### Basses(s)
+ ServiceException
### SubElement(s)
 > ## Function  `__init__`
## Class `EmptyCommandsException`
```text
Empty list of commands for service operation
```

### Basses(s)
+ ServiceException
### SubElement(s)
 > ## Function  `__init__`
## Class `NotUniqueCommandError`
```text
Class error if user add the same commands
```

### Basses(s)
+ ServiceException
## Class `ServiceBuilderException`
```text
Class for exceptions in BuilderService
```

### Basses(s)
+ ServiceException
## Class `IncorrectDefaultCommand`
```text
Among the available commands, there is no default command
```

### Basses(s)
+ ServiceException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `command`: str - empty doc string
 > + `list_command`: List[str]
 > - empty doc string
## Class `StepperException`
```text
Main exception class exceptions with Stepper
```

### Basses(s)
+ OrchServError
## Class `NoDataForExecutionStepException`
```text
Exception for empty response
```

### Basses(s)
+ StepperException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `step`: str - empty doc string
## Class `ConsistencyStepsException`
```text
handling attribute error
for cases when the data returned by the
previous object + additional arguments declared during
block initialization do not fit the method structure
```

### Basses(s)
+ StepperException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `step`: str - empty doc string
 > + `previous_step`: str - empty doc string
 > + `signature_step_obj`: str - empty doc string
 > + `return_annotation_previous_step_obj`: str - empty doc string
 > + `received_from_previous_step`: Any - empty doc string
 > + `args_on_init_step`: Any - empty doc string
## Class `DataConsistencyError`
```text
Error when expected and passed data do not match
```

### Basses(s)
+ StepperException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `obj`: str - empty doc string
 > + `errors`: List[str]
 > - empty doc string
## Class `ExtraAttributeError`
```text
If in kwargs for function provided extra attributes
```

### Basses(s)
+ StepperException
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `obj`: str - empty doc string
 > + `extra_attributes`: List[str]
 > - empty doc string
 > + `obj_attributes`: str - empty doc string