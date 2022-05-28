"""
Module with base msg for processing
"""
# pylint: disable=too-few-public-methods,no-name-in-module

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

SubPydanticBodyModel = TypeVar("SubPydanticBodyModel", bound=BaseModel)
SubPydanticHeaderModel = TypeVar("SubPydanticHeaderModel", bound=BaseModel)


class BaseOrchServMsg(
    GenericModel, Generic[SubPydanticBodyModel, SubPydanticHeaderModel]
):
    """
    Base message class for processing and to use the library
    :attr body:
    :type SubPydanticBodyModel:
    :attr header:
    :type SubPydanticHeaderModel:
    :example:
    >>> # How to use BaseOrchServMsg to create a custom message for your needs
    >>> # The first step: create body model your msg
    >>> from pydantic import BaseModel
    >>> class MyBody(BaseModel):
    >>>     body_option: str # any type you need
    >>> # The second step: create header model your
    >>> # msg (is optional if you need a header)
    >>> class MyHeader(BaseModel):
    >>>     header_option: str # any type you need
    >>> # The third step: create your msg
    >>> # The first option:
    >>> MyTypeFir = BaseOrchServMsg[MyBody, MyHeader]
    >>> example_my_type = {"body": {
    >>>                         "body_option": "test_body"},
    >>>                    "header":{
    >>>                          "header_option":"test_header"}}
    >>> my_value = MyTypeFir(**example_my_type)
    >>> # First option without header
    >>> MyTypeFirWithoutHeader = BaseOrchServMsg[MyBody, BaseModel]
    >>> # The second option
    >>> class MyTypeSec(BaseOrchServMsg):
    >>>     body: MyBody
    >>>     header: MyHeader
    >>> MyTypeSec(**example_my_type)
    """

    body: SubPydanticBodyModel = Field(
        ..., description="The body of the message with the " "structure you need"
    )
    header: Optional[SubPydanticHeaderModel] = Field(
        description="Optional message header " "with the structure you need"
    )
