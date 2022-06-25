# Module `stepper.py`
> Path: `orch_serv\stepper\stepper.py`
## Class `Step`
```text
Class for configuration Step of Stepper flow
```

### Attributes(s)
+ __obj`:Callable - obj object that contains logic
+ __kwargs`:Dict[str, Any] - additional kwargs for execution step
which are not returned from the previous step
### Example 
```python
>>> def example_function(val: int , arg_1: int = 1) -> int:
>>>     return val + arg_1
>>> step_1 = Step(example_function )
>>> step_1.execute(1) # return: 2
>>> step_2 = Step(example_function, arg_1=2 )
>>> step_1.execute(1) # return: 3
```

### SubElement(s)
 > `__obj`: Callable = None
 > `__kwargs`: Dict[str, Any] = dict()
 > ## Function  `obj`
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Callable`
 > ## Function  `kwargs`
 > ### Decorator(s)
 > + property
 > #### Declared returns: `Dict[str, Any]`
 > ## Function  `__init__`
 > ### Argument(s)
 > + `obj`: Callable - empty doc string
 > + **`kwargs` - empty doc string
 > ## Function  `__repr__`
 > ## Function  `__str__`
 > ## Function  `execute`
 > ### Argument(s)
 > + `data_to_execute`: Any - empty doc string
 > #### Declared returns: `Any`
## Class `StepsBuilder`
```text
Class for build and handling steps
```

### Attributes(s)
+ __steps`:List[Step] - steps flow
### Example 
```python
>>> step_builder = StepsBuilder(
>>>    Step(function1),
>>>    Step(function2),
>>>    is_validate_consistency_steps=True)
```

### SubElement(s)
 > `__steps`: List[Step] = None
 > ## Function  `__init__`
 > ```text
 > Init StepBuilder
 > ```
 > 
 > ### Argument(s)
 > + `is_validate_consistency_steps`: bool - whether to check
 > the consistency of steps by types
 > and attributes or not
 > !!! Attention !!!
 > Used for methods with type annotation
 > if you are not using type annotations then start or pass a value to False.
 > !!! Then we are not responsible for the complete correctness of your data.
 > + *`steps`: Step - List of steps
 > ## Function  `steps`
 > ### Decorator(s)
 > + property
 > #### Declared returns: `List[Step]`
 > ## Function  `__iter__`
 > ## Function  `__len__`
 > ## Function  `__getitem__`
 > ### Argument(s)
 > + `index` - empty doc string
## Class `StepsIterator`
### SubElement(s)
 > ## Function  `__init__`
 > ### Argument(s)
 > + `steps`: StepsBuilder - empty doc string
 > ## Function  `__next__`
 > #### Declared returns: `Step`
## Class `Stepper`
```text
class for forming a flow where the input data
of step n is the output of step n
```

### SubElement(s)
 > `__steps`: StepsBuilder = None
 > `__is_execute_if_empty`: bool = False
 > ## Function  `steps`
 > ```text
 > Property contains a class with all blocks for the current flow
 > ```
 > 
 > ### Decorator(s)
 > + property
 > ### Return
 > ```text
 > StepsBuilder
 > ```
 > 
 > #### Declared returns: `StepsBuilder`
 > ## Function  `is_execute_if_empty`
 > ```text
 > execute the next step with the data of the previous one
 > if the current step did not return anything
 > ```
 > 
 > ### Decorator(s)
 > + property
 > #### Declared returns: `bool`
 > ## Function  `__init__`
 > ### Argument(s)
 > + `steps`: Optional[StepsBuilder] - empty doc string
 > + `is_execute_if_empty`: Optional[bool] - empty doc string
 > + `logger`: Optional[Logger] - empty doc string
 > ## Function  `__step_by_step`
 > ### Argument(s)
 > + *`args`: Any - empty doc string
 > #### Declared returns: `Any`
 > ## Function  `step_by_step`
 > ### Argument(s)
 > + *`args`: Any - empty doc string
 > #### Declared returns: `Any`