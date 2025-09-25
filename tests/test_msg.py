"""
Test msg library
"""
# pylint: disable=too-few-public-methods,no-name-in-module,invalid-name,abstract-method
from typing import Dict, Optional, Type, Union

import pytest
from pydantic import BaseModel, ValidationError

from orch_serv import BaseOrchServMsg


class BodyModel(BaseModel):
    """
    Body model for test
    """

    body_option: Optional[str] = None


class HeaderModel(BaseModel):
    """
    Header model for test
    """

    header_option: Optional[str] = None


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
        return body.model_dump()
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
        return header.model_dump()
    return header


def tst_full(obj_type: Type[BaseOrchServMsg], is_optional_header: bool = False) -> None:
    """
    Method to test the type with full fields
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
    assert data_to_compare == val1.model_dump()
    assert data_to_compare == val2.model_dump()
    assert data_to_compare == val3.model_dump()
    assert data_to_compare == val4.model_dump()
    assert data_to_compare == val5.model_dump()
    assert isinstance(val1.body, BodyModel)
    assert isinstance(val1.header, HeaderModel)


def tst_body(obj_type: Type[BaseOrchServMsg]) -> None:
    """
    Function test types with body only
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
    assert data_to_compare == val1.model_dump()
    assert data_to_compare == val2.model_dump()
    assert data_to_compare == val3.model_dump()
    assert isinstance(val1.body, BodyModel)
    assert not isinstance(val1.header, HeaderModel)


def test_inheritance() -> None:
    """
    Test correctness of types if inheritance base msg model
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
    Test correctness of types if you substitute types in generic
    :return:
    """
    MyType = BaseOrchServMsg[BodyModel, HeaderModel]
    assert issubclass(MyType, BaseOrchServMsg)
    tst_full(MyType, is_optional_header=True)
    MyTypeWithoutHeader = BaseOrchServMsg[BodyModel, BodyModel]
    tst_body(MyTypeWithoutHeader)


def test_msg_source():
    """
    test set|get source to msg
    :return:
    """
    test_source = "test_source"

    class MyTypeInvalid(BaseOrchServMsg):
        """
        Test class
        """

        body: BodyModel
        header: HeaderModel

    val = MyTypeInvalid(header=header_data(), body=body_data())
    with pytest.raises(NotImplementedError):
        val.get_source()
    with pytest.raises(NotImplementedError):
        val.set_source(test_source)

    class HeaderModelWithSource(BaseModel):
        """
        test class
        """

        source: Optional[str] = None

    class CorrectMsg(BaseOrchServMsg):
        """
        test class
        """

        body: BodyModel
        header: HeaderModelWithSource

        def set_source(self, source: str) -> None:
            self.header.source = source

        def get_source(self) -> str:
            return self.header.source

    val = CorrectMsg(body=body_data(), header=dict())
    val.set_source(source=test_source)
    assert val.get_source() == test_source


def test_get_flow() -> None:
    class MyTypeInvalid(BaseOrchServMsg):
        """
        Test class
        """

        body: BodyModel
        header: HeaderModel

    val = MyTypeInvalid(header=header_data(), body=body_data())
    with pytest.raises(NotImplementedError):
        val.get_flow()

    class HeaderModelWithSource(BaseModel):
        """
        test class
        """

        source: Optional[str] = None
        flow: Optional[str] = None

    class CorrectMsg(BaseOrchServMsg):
        """
        test class
        """

        body: BodyModel
        header: HeaderModelWithSource

        def get_flow(self) -> str:
            return self.header.flow

    test_flow = "test_flow"
    val = CorrectMsg(body=body_data(), header=dict(flow=test_flow))

    assert val.get_flow() == test_flow


def test_get_target() -> None:
    class MyTypeInvalid(BaseOrchServMsg):
        """
        Test class
        """

        body: BodyModel
        header: HeaderModel

    val = MyTypeInvalid(header=header_data(), body=body_data())
    with pytest.raises(NotImplementedError):
        val.get_target()

    class HeaderModelWithSource(BaseModel):
        """
        test class
        """

        target: Optional[str]

    class CorrectMsg(BaseOrchServMsg):
        """
        test class
        """

        body: BodyModel
        header: HeaderModelWithSource

        def get_target(self) -> str:
            return self.header.target

    test_target = "test_target"
    val = CorrectMsg(body=body_data(), header=dict(target=test_target))

    assert val.get_target() == test_target


def test_get_command() -> None:
    class MyTypeInvalid(BaseOrchServMsg):
        """
        Test class
        """

        body: BodyModel
        header: HeaderModel

    val = MyTypeInvalid(header=header_data(), body=body_data())
    with pytest.raises(NotImplementedError):
        val.get_command()

    class HeaderModelWithSource(BaseModel):
        """
        test class
        """

        command: Optional[str]

    class CorrectMsg(BaseOrchServMsg):
        """
        test class
        """

        body: BodyModel
        header: HeaderModelWithSource

        def get_command(self) -> str:
            return self.header.command

    test_command = "test_command"
    val = CorrectMsg(body=body_data(), header=dict(command=test_command))

    assert val.get_command() == test_command
