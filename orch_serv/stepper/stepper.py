from abc import ABC
from copy import deepcopy
from logging import Logger
from typing import Any, Callable, Dict, List, Optional

from orch_serv.exc import ConsistencyStepsException, NoDataForExecutionStepException
from orch_serv.settings import DEFAULT_LOGGER
from orch_serv.stepper.utils import (
    get_returned_value,
    parse_signature,
    validation_data_consistency,
)


class Step:
    """ """

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

    def __repr__(self):  # pragma: no cover
        return str(self)

    def __str__(self):
        return f"<Step: obj: {self.obj.__name__}; kwargs:{self.__kwargs}>"


class StepsBuilder:
    __steps: List[Step]
    __position: int

    def __init__(self, *steps: Step, is_validate_consistency_steps: bool = True):
        """
        Init StepBuilder
        :param steps: List of steps
        :type steps: *Step
        :param is_validate_consistency_steps: whether to check
         the consistency of steps by types
         and attributes or not
        :type is_validate_consistency_steps: bool default: True
        """
        self.__steps = list()
        self.__position = 0
        if not isinstance(steps[0], Step):  # pragma: no cover
            raise TypeError(f"Step must be a Step and not {type(steps[0])}")
        self.__steps.append(steps[0])
        returned_previous_steps = get_returned_value(steps[0].obj)
        for step in steps[1:]:
            if not isinstance(step, Step):
                raise TypeError(f"Step must be a Step and not {type(step)}")
            if is_validate_consistency_steps:  # pragma: no cover
                validation_data_consistency(
                    obj=step.obj,
                    return_previous_obj=returned_previous_steps,
                    additional_args=deepcopy(step.kwargs),
                )
                returned_previous_steps = get_returned_value(step.obj)
            self.__steps.append(step)

    @property
    def steps(self) -> List[Step]:
        return self.__steps

    def __next__(self) -> Step:
        if self.__position < len(self.__steps):
            value = self.__steps[self.__position]
            self.__position += 1
            return value
        else:
            raise StopIteration

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.__steps)

    def __getitem__(self, index):
        return self.__steps[index]


class Stepper(ABC):
    @property
    def steps(self) -> StepsBuilder:  # pragma: no cover
        """
        Property contains a class with all blocks for the current flow
        :return: StepsBuilder
        """
        raise NotImplementedError

    @property
    def is_execute_if_empty(self) -> bool:
        """
        execute the next step with the data of the previous one
         if the current step did not return anything
        :return:
        """
        return False

    def __init__(self, logger: Optional[Logger] = None):
        self.logger = logger or DEFAULT_LOGGER

    def __step_by_step(
        self,
        *args: Any,
    ) -> Any:
        step_data = args
        previous_step = "start"
        result_data: Any = None
        for i, step in enumerate(self.steps):
            try:
                if not isinstance(step_data, tuple):
                    step_data = (step_data,)
                result_data = step.obj(*step_data, **step.kwargs)
                if not result_data and not self.is_execute_if_empty:
                    raise NoDataForExecutionStepException(
                        step.obj.__name__,
                    )
                elif not result_data:
                    continue
                else:
                    step_data = result_data
                    previous_step = step.obj.__name__

            except (AttributeError, TypeError):
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
        return result_data

    def step_by_step(
        self,
        *args: Any,
    ) -> Any:
        return self.__step_by_step(*args)


# ToDo add if else and loop !
