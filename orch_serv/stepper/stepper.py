from __future__ import annotations

from copy import deepcopy
from logging import Logger
from typing import Any, Callable, Dict, List, Optional

from orch_serv.exc import ConsistencyStepsException, NoDataForExecutionStepException
from orch_serv.settings import DEFAULT_LOGGER
from orch_serv.stepper.utils import (
    get_returned_value,
    parse_signature,
    validate_data_consistency,
    validate_data_step,
)


class Step:
    """
    Class for configuration Step of Stepper flow
    :attr __obj: obj object that contains logic
    :type __obj: Callable
    :attr __kwargs: additional kwargs for execution step
     which are not returned from the previous step
    :type __kwargs: Dict[str, Any]
    :example:
    >>> def example_function(val: int , arg_1: int = 1) -> int:
    >>>     return val + arg_1
    >>> step_1 = Step(example_function )
    >>> step_1.execute(1) # return: 2
    >>> step_2 = Step(example_function, arg_1=2 )
    >>> step_1.execute(1) # return: 3

    """

    __obj: Callable = None
    __kwargs: Dict[str, Any] = dict()

    @property
    def obj(self) -> Callable:
        return self.__obj

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self.__kwargs

    def __init__(self, obj: Callable, **kwargs):
        if not callable(obj):
            raise TypeError("Step `obj` must be a callable")
        self.__obj = obj  # type: ignore
        if kwargs:
            self.__kwargs = kwargs
        validate_data_step(self.__obj, self.__kwargs)

    def __repr__(self):  # pragma: no cover
        return str(self)

    def __str__(self):
        return f"<Step: obj: {self.obj.__name__}; kwargs:{self.__kwargs}>"

    def execute(self, data_to_execute: Any) -> Any:
        if not isinstance(data_to_execute, tuple):
            data_to_execute = (data_to_execute,)
        return self.obj(*data_to_execute, **self.kwargs)


class StepsBuilder:
    """
    Class for build and handling steps
    :attr __steps: steps flow
    :type __steps: List[Step]
    :example:
    >>> step_builder = StepsBuilder(
    >>>    Step(function1),
    >>>    Step(function2),
    >>>    is_validate_consistency_steps=True)
    """

    __steps: List[Step]

    def __init__(self, *steps: Step, is_validate_consistency_steps: bool = True):
        """
        Init StepBuilder
        :param steps: List of steps
        :type steps: *Step
        :param is_validate_consistency_steps: whether to check
         the consistency of steps by types
         and attributes or not
         !!! Attention !!!
         Used for methods with type annotation
         if you are not using type annotations then start or pass a value to False.
         !!! Then we are not responsible for the complete correctness of your data.
        :type is_validate_consistency_steps: bool default: True
        """
        self.__steps = list()
        if not isinstance(steps[0], Step):  # pragma: no cover
            raise TypeError(f"Step must be a Step and not {type(steps[0])}")
        self.__steps.append(steps[0])
        returned_previous_steps = get_returned_value(steps[0].obj)
        for step in steps[1:]:
            if not isinstance(step, Step):
                raise TypeError(f"Step must be a Step and not {type(step)}")
            if is_validate_consistency_steps:  # pragma: no cover
                validate_data_consistency(
                    obj=step.obj,
                    return_previous_obj=returned_previous_steps,
                    additional_args=deepcopy(step.kwargs),
                )
                returned_previous_steps = get_returned_value(step.obj)
            self.__steps.append(step)

    @property
    def steps(self) -> List[Step]:
        return self.__steps

    def __iter__(self):
        return StepsIterator(self)

    def __len__(self):
        return len(self.__steps)

    def __getitem__(self, index):
        return self.__steps[index]


class StepsIterator:
    def __init__(self, steps: StepsBuilder):
        if not isinstance(steps, StepsBuilder):
            raise TypeError
        self.__position = 0
        self.__steps = steps.steps

    def __next__(self) -> Step:
        if self.__position < len(self.__steps):
            value = self.__steps[self.__position]
            self.__position += 1
            return value
        else:
            raise StopIteration


class Stepper:
    """
    class for forming a flow where the input data
     of step n is the output of step n
    """

    __steps: StepsBuilder = None
    __is_execute_if_empty: bool = False

    @property
    def steps(self) -> StepsBuilder:  # pragma: no cover
        """
        Property contains a class with all blocks for the current flow
        :return: StepsBuilder
        """
        if self.__steps:  # pragma: no cover
            return self.__steps
        raise NotImplementedError

    @property
    def is_execute_if_empty(self) -> bool:
        """
        execute the next step with the data of the previous one
         if the current step did not return anything
        :return:
        """
        return self.__is_execute_if_empty

    def __init__(
        self,
        steps: Optional[StepsBuilder] = None,
        is_execute_if_empty: Optional[bool] = None,
        logger: Optional[Logger] = None,
    ):
        self.logger = logger or DEFAULT_LOGGER
        if steps:
            self.__steps = steps
        if not (is_execute_if_empty is None):
            self.__is_execute_if_empty = is_execute_if_empty
        if not isinstance(self.steps, StepsBuilder):
            raise TypeError(
                f"`Stepper.steps` must be a StepsBuilder and not {type(self.steps)} "
            )

    def __step_by_step(
        self,
        *args: Any,
    ) -> Any:
        step_data = args
        previous_step = "start"
        result_data: Any = None
        for i, step in enumerate(self.steps):
            self.logger.info("Starting Step %s", step)
            try:
                # if not isinstance(step_data, tuple):
                #     step_data = (step_data,)
                # result_data = step.obj(*step_data, **step.kwargs)
                result_data = step.execute(step_data)
                if not result_data and not self.is_execute_if_empty:
                    raise NoDataForExecutionStepException(
                        step.obj.__name__,
                    )
                elif not result_data:
                    continue
                else:
                    step_data = result_data
                    previous_step = step.obj.__name__

            except (AttributeError, TypeError) as exc:
                self.logger.error(
                    "Error in time processing %s. "
                    "Inconsistency of arguments for function "
                    "execution or internal object error."
                    " Error: %s",
                    step,
                    str(exc),
                    exc_info=True,
                )
                params_prev, return_prev = parse_signature(self.steps[i - 1].obj)
                params_current, return_current = parse_signature(self.steps[i].obj)
                raise ConsistencyStepsException(
                    step=self.steps[i].obj.__name__,
                    previous_step=previous_step,
                    signature_step_obj=params_current,
                    return_annotation_previous_step_obj=return_prev,
                    received_from_previous_step=step_data,
                    args_on_init_step=str(self.steps[i].kwargs),
                )
            except Exception as exc:
                self.logger.error(
                    "Error in time processing %s. Error: %s", step, str(exc)
                )
                raise exc

            self.logger.info("Finished Step %s", step)

        return result_data

    def step_by_step(
        self,
        *args: Any,
    ) -> Any:
        return self.__step_by_step(*args)


# ToDo add if else and loop !
