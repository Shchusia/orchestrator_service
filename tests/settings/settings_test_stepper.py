from typing import Any, List, Optional, Tuple

from orch_serv import Step, Stepper, StepsBuilder


def tst_function() -> Tuple[int, int]:
    pass


def tst_function_2(val1: str, val2: int, arg1: int, arg2: int) -> None:
    pass


def tst_function_3(val1: int, val2: int, arg1: int = 1, arg2: int = 2) -> None:
    pass


def tst_function_4(
    val1: int, val2: int, arg1: int = 1, arg2: int = 2, **kwargs: Any
) -> None:
    pass


class TestClass:
    """test class"""


LIST_ARGS = []


def correct_step_1() -> List[int]:
    LIST_ARGS.append(1)
    new_array = [1, 2, 3]
    return new_array


def correct_step_2(value: List[int], arg: int = 1) -> List[int]:
    LIST_ARGS.append(value[0])
    LIST_ARGS.append(arg)
    return value[1:]


def correct_step_3_without_response(  # type: ignore
    value: List[int], arg: int = 1
) -> Optional[List[int]]:  # noqa
    LIST_ARGS.append(value[0])
    LIST_ARGS.append(arg)


class MyFirstFlow(Stepper):
    steps = StepsBuilder(
        Step(correct_step_1),
        Step(correct_step_2),
        Step(correct_step_3_without_response),
        Step(correct_step_2, arg=2),
    )


class MySecondFlow(Stepper):
    steps = StepsBuilder(
        Step(correct_step_1),
        Step(correct_step_2),
        Step(correct_step_3_without_response),
        Step(correct_step_2, arg=2),
    )
    is_execute_if_empty = True


class MyThirdFlow(Stepper):
    steps = StepsBuilder(
        Step(correct_step_1),
        Step(correct_step_2),
        Step(correct_step_1),
    )
    is_execute_if_empty = True


DATA_AFTER_FIRST_FLOW = [1, 1, 1, 2, 1]
DATA_AFTER_SECOND_FLOW = [1, 1, 1, 2, 1, 2, 2]


def tst_function_with_optional() -> Optional[int]:
    pass


def tst_function_with_optional_2(val: int) -> None:
    pass
