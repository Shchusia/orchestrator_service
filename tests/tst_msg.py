"""
Test msg library
"""
# pylint: disable=too-few-public-methods,no-name-in-module,invalid-name
from typing import Dict, Type, Union

import pytest
from pydantic import BaseModel, ValidationError

from orch_serv import BaseOrchServMsg


class BodyModel(BaseModel):
    """
    Body model for test
    """

    body_option: str


class HeaderModel(BaseModel):
    """
    Header model for test
    """

    header_option: str


def body_data(is_raw: bool = True) -> Union[Dict[str, str], BodyModel]:
    """
    Texture for body data
    :param is_raw: if true return raw dict else return instance BodyModel
    :type is_raw: bool
    :return: data for test body
    :rtype: Union[Dict[str, str], BodyModel]
    """
    body = BodyModel(body_option="test_body")
    if is_raw:
        return body.dict()
    return body


def header_data(is_raw: bool = True) -> Union[Dict[str, str], HeaderModel]:
    """
    Texture for header data
    :param is_raw: if true return raw dict else return instance HeaderModel
    :type is_raw: bool
    :return: data for test header
    :rtype: Union[Dict[str, str], HeaderModel]
    """
    header = HeaderModel(header_option="test_header")
    if is_raw:
        return header.dict()
    return header


def tst_full(obj_type: Type[BaseOrchServMsg], is_optional_header: bool = False) -> None:
    """
    Method to test on type with full fields
    :param obj: type to test correct validation
    :type obj: Type[BaseOrchServMsg]
    :param is_optional_header: use for generic type
    :type is_optional_header: bool

    :return: nothing
    """
    if not is_optional_header:
        with pytest.raises(ValidationError):
            # without header
            obj_type(body=body_data())
    with pytest.raises(ValidationError):
        # without body
        obj_type(header=header_data())
    val1 = obj_type(body=body_data(is_raw=True), header=header_data(is_raw=True))
    val2 = obj_type(body=body_data(is_raw=False), header=header_data(is_raw=True))
    val3 = obj_type(body=body_data(is_raw=False), header=header_data(is_raw=False))
    val4 = obj_type(body=body_data(is_raw=True), header=header_data(is_raw=False))
    data_to_compare = dict(body=body_data(is_raw=True), header=header_data())
    val5 = obj_type(**data_to_compare)
    assert isinstance(val1, BaseOrchServMsg)
    assert isinstance(val2, BaseOrchServMsg)
    assert isinstance(val3, BaseOrchServMsg)
    assert isinstance(val4, BaseOrchServMsg)
    assert data_to_compare == val1.dict()
    assert data_to_compare == val2.dict()
    assert data_to_compare == val3.dict()
    assert data_to_compare == val4.dict()
    assert data_to_compare == val5.dict()
    assert isinstance(val1.body, BodyModel)
    assert isinstance(val1.header, HeaderModel)


def tst_body(obj_type: Type[BaseOrchServMsg]) -> None:
    """
    Function test types with only body
    :param obj_type: type to test
    :return: nothing
    """
    with pytest.raises(ValidationError):
        # without body
        obj_type(header=header_data())

    val1 = obj_type(body=body_data(is_raw=True))
    val2 = obj_type(body=body_data(is_raw=False))
    data_to_compare = dict(body=body_data(is_raw=True), header=None)
    val3 = obj_type(**data_to_compare)
    assert isinstance(val1, BaseOrchServMsg)
    assert isinstance(val2, BaseOrchServMsg)
    assert isinstance(val3, BaseOrchServMsg)
    assert data_to_compare == val1.dict()
    assert data_to_compare == val2.dict()
    assert data_to_compare == val3.dict()
    assert isinstance(val1.body, BodyModel)
    assert not isinstance(val1.header, HeaderModel)


def test_inheritance() -> None:
    """
    Test correct types if inheritance base msg model
    :return: nothing
    """

    class MyType(BaseOrchServMsg):
        """
        Test class
        """

        body: BodyModel
        header: HeaderModel

    assert issubclass(MyType, BaseOrchServMsg)
    tst_full(MyType)

    class MyTypeWithoutHeader(BaseOrchServMsg):
        """
        test class
        """

        body: BodyModel

    assert issubclass(MyTypeWithoutHeader, BaseOrchServMsg)
    tst_body(MyTypeWithoutHeader)


def test_generic():
    """
    Test correct types if you substitute types in generic
    :return:
    """
    MyType = BaseOrchServMsg[BodyModel, HeaderModel]
    assert issubclass(MyType, BaseOrchServMsg)
    tst_full(MyType, is_optional_header=True)
    MyTypeWithoutHeader = BaseOrchServMsg[BodyModel, BodyModel]
    tst_body(MyTypeWithoutHeader)
