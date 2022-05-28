"""
Example how create message
"""
# pylint: disable=too-few-public-methods,no-name-in-module
from pydantic import BaseModel

from orch_serv import BaseOrchServMsg


class BodyModel(BaseModel):
    """
    Example body model
    """

    body_option_1: str
    body_option_2: str


class HeaderModel(BaseModel):
    """
    Example header model
    """

    header_option: str


DATA_TO_TEST = dict(
    body=dict(body_option_1="body_option_1", body_option_2="body_option_2"),
    header=dict(header_option="header_option"),
)


class MyFirstExampleCustomMessage(BaseOrchServMsg):
    """
    Example how create msg with your structure the first option
    """

    body: BodyModel
    header: HeaderModel


# Example how create msg with your structure the second option
MySecondExampleCustomMessage = BaseOrchServMsg[BodyModel, HeaderModel]

val_first_model = MyFirstExampleCustomMessage(**DATA_TO_TEST)
val_second_model = MySecondExampleCustomMessage(**DATA_TO_TEST)

assert isinstance(val_first_model, BaseOrchServMsg)
assert isinstance(val_second_model, BaseOrchServMsg)
assert val_first_model.dict() == val_second_model.dict()
