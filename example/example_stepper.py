"""
Example how use work stepper
"""
from typing import List, Tuple

from orch_serv import Step, Stepper, StepsBuilder


def function_get_data() -> List[int]:
    """synthetic example"""
    # do something logic
    return [1, 2, 3]


def split_into_head_and_tail(data: List[int]) -> Tuple[int, List[int]]:
    """synthetic example"""
    # do something logic
    return data[0], data[1:]


def print_data(head: int, tail: List[int], additional_arg: int = 1) -> List[int]:
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
print("response:", mlf.step_by_step())
