# Stepper

> the module contains classes for forming sequences of function execution. where the input of step n is the output of
> step n-1

## Creation

### Function for execution

```python
def function_1() -> int:
    pass


def function_2(val: int, arg: int = 1) -> int:
    pass 
```

### Step(s)

> steps from which your flow will be built

> the class validates the passed named arguments for the function. if there are extras, an exception will be
> thrown `ExtraAttributeError`

```python
from orch_serv import Step

step1 = Step(function_1)
step2 = Step(function_2, arg=2)
```

### StepBuilder

> steps aggregator

> steps must be submitted in the order in which they are performed

> the aggregator checks the consistency of the types of the input and output parameters of the function according to the
> type annotation

> if you are not using the annotation you can disable it by passing an argument `is_validate_consistency_steps` = False
> checked by default

```python
from orch_serv import StepsBuilder

steps_builder = StepsBuilder(step1,
                             step2,
                             is_validate_consistency_steps=True)
```

### InitStepper

> The main class that executes the logic and starts the execution of the steps

>  If some object does not return data, then the execution chain is interrupted. 
> But if it is planned that way, then you can fix it by changing the initialization of Stepper by passing the values `is_execute_if_empty=True`
> Then the data from the previous step when they were returned will be transferred to the step.

```python
from orch_serv import Stepper

stepper = Stepper(steps)
stepper.step_by_step()
```

### [MoreExamples](../../example/example_stepper.py)