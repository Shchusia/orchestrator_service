"""
Example how use work stepper
"""
from typing import List, Optional, Tuple

from orch_serv import Step, Stepper, StepsBuilder

print("Example use 1")


def function_get_data() -> list[int]:
    """synthetic example"""
    # do something logic
    return [1, 2, 3]


def split_into_head_and_tail(data: list[int]) -> tuple[int, list[int]]:
    """synthetic example"""
    # do something logic
    return data[0], data[1:]


def print_data(head: int, tail: list[int], additional_arg: int = 1) -> list[int]:
    """synthetic example"""
    print("Head: ", head, "Tail: ", tail, "Additional arguments: ", additional_arg)
    return tail


class MyLogicFlow(Stepper):
    """your class"""

    steps = StepsBuilder(
        Step(function_get_data),
        Step(split_into_head_and_tail),
        Step(print_data),
        Step(split_into_head_and_tail),
        Step(print_data, additional_arg=2),
        is_validate_consistency_steps=True,
    )


mlf = MyLogicFlow()
print("result:", mlf.step_by_step())

print("Example use 2")
AGGREGATOR = list()


def second_example_function_1(val1: int) -> Optional[int]:
    val1 += 1
    AGGREGATOR.append(val1)
    return None


def second_example_function_2(val1: int) -> Optional[int]:
    val1 += 1
    AGGREGATOR.append(val1)
    return val1


step_builder = StepsBuilder(
    Step(second_example_function_1),
    Step(second_example_function_2),
)
stepper = Stepper(steps=step_builder, is_execute_if_empty=True)
print("result:", stepper.step_by_step(1))
print("aggregated:", AGGREGATOR)
