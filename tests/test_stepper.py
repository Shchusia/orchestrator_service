"""
Module with tests orch_serv.stepper.stepper
"""

import pytest

from orch_serv.exc import (
    ConsistencyStepsException,
    DataConsistencyError,
    ExtraAttributeError,
    NoDataForExecutionStepException,
    EmptyStepper,
)
from orch_serv.stepper.stepper import Step, Stepper, StepsBuilder
from tests.settings.settings_test_stepper import (
    DATA_AFTER_FIRST_FLOW,
    DATA_AFTER_SECOND_FLOW,
    LIST_ARGS,
    MyFirstFlow,
    MySecondFlow,
    MyThirdFlow,
    TestClass,
    tst_function,
    tst_function_2,
    tst_function_3,
    tst_function_4,
    tst_function_with_optional,
    tst_function_with_optional_2,
)


def test_stepper() -> None:
    """
    tests for stepper
        :return:
    """
    with pytest.raises(TypeError):
        Step(42)  # type: ignore
    with pytest.raises(TypeError):
        Step(42, val1=1, val2=2)  # type: ignore

    with pytest.raises(TypeError):
        StepsBuilder(Step(tst_function), TestClass())  # type: ignore
    with pytest.raises(DataConsistencyError):
        StepsBuilder(Step(tst_function), Step(tst_function_2))
    with pytest.raises(DataConsistencyError):
        StepsBuilder(Step(tst_function), Step(tst_function_2, arg1=1))
    with pytest.raises(DataConsistencyError):
        StepsBuilder(Step(tst_function), Step(tst_function_2, arg1=1, arg2=2))
    with pytest.raises(ExtraAttributeError):
        StepsBuilder(Step(tst_function), Step(tst_function_2, arg3=3))
    with pytest.raises(ExtraAttributeError):
        StepsBuilder(Step(tst_function), Step(tst_function_3, arg3=3, val1=1))
    StepsBuilder(Step(tst_function), Step(tst_function_4, arg3=3, val1=1))
    with pytest.raises(ExtraAttributeError):
        Step(tst_function, val1=1)
    with pytest.raises(ExtraAttributeError):
        Step(tst_function_2, val1=1, arg1=1, arg3=3)

    s1 = Step(tst_function)
    s2 = Step(tst_function_3)

    st = StepsBuilder(s1, s2)
    assert len(st) == 2
    assert len(st) == len(st.steps)
    assert s1 == st[0]
    assert s2 == st[1]
    assert isinstance(st.steps, list)

    sb1 = StepsBuilder(Step(tst_function), Step(tst_function_3, val1=1))
    StepsBuilder(Step(tst_function), Step(tst_function_3, arg1=1))
    StepsBuilder(
        Step(tst_function),
        Step(tst_function_3, arg1=1, arg2=2),
        is_validate_consistency_steps=True,
    )

    with pytest.raises(NoDataForExecutionStepException):
        MyFirstFlow().step_by_step()
    with pytest.raises(TypeError):
        Stepper(steps=s1)  # type: ignore
    with pytest.raises(NotImplementedError):
        Stepper()

    with pytest.raises(EmptyStepper):
        StepsBuilder()
    assert Stepper.is_execute_if_empty != Stepper(steps=sb1, is_execute_if_empty=True)

    assert LIST_ARGS == DATA_AFTER_FIRST_FLOW
    with pytest.raises(ConsistencyStepsException):
        MyThirdFlow().step_by_step()
    LIST_ARGS.clear()
    resp = MySecondFlow().step_by_step()
    assert LIST_ARGS == DATA_AFTER_SECOND_FLOW
    assert resp == [3]

    StepsBuilder(Step(tst_function_with_optional), Step(tst_function_with_optional_2))
