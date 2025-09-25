from collections.abc import Callable
import enum
import inspect
from types import MappingProxyType
from typing import Any, Union, get_args, get_origin
import warnings

from orch_serv.exc import DataConsistencyError, ExtraAttributeError


class ParameterKind(enum.IntEnum):
    POSITIONAL_ONLY = 0
    POSITIONAL_OR_KEYWORD = 1
    VAR_POSITIONAL = 2
    KEYWORD_ONLY = 3
    VAR_KEYWORD = 4


def format_signature_parameters(
    parameters: MappingProxyType[str, inspect.Parameter],
) -> str:
    """
    Method copied from inspect for private usage
    """
    result = []
    render_pos_only_separator = False
    render_kw_only_separator = True
    for param in parameters.values():
        formatted = str(param)

        kind = param.kind

        if kind == ParameterKind.POSITIONAL_ONLY.value:
            render_pos_only_separator = True  # pragma: no cover
        elif render_pos_only_separator:  # pragma: no cover
            # It's not a positional-only parameter, and the flag
            # is set to 'True' (there were pos-only params before.)
            result.append("/")
            render_pos_only_separator = False

        if kind == ParameterKind.VAR_POSITIONAL.value:
            # OK, we have an '*args'-like parameter, so we won't need
            # a '*' to separate keyword-only arguments
            render_kw_only_separator = False  # pragma: no cover
        elif (
            kind == ParameterKind.KEYWORD_ONLY.value and render_kw_only_separator
        ):  # pragma: no cover
            # We have a keyword-only parameter to render and we haven't
            # rendered an '*args'-like parameter before, so add a '*'
            # separator to the parameters list ("foo(arg1, *, arg2)" case)
            result.append("*")
            # This condition should be only triggered once, so
            # reset the flag
            render_kw_only_separator = False

        result.append(formatted)

    if render_pos_only_separator:
        # There were only positional-only parameters, hence the
        # flag was not reset to 'False'
        result.append("/")  # pragma: no cover

    return ", ".join(result)


def parse_signature(obj: Callable) -> tuple[str, str]:
    """
    parse_signature of obj
    :param obj:
    :return: (attributes, returned)
    """
    signature = inspect.signature(obj)
    return format_signature_parameters(signature.parameters), inspect.formatannotation(  # type: ignore
        signature.return_annotation
    )


def get_returned_value(obj: Callable) -> Any:
    signature = inspect.signature(obj)
    if get_origin(signature.return_annotation) is tuple:
        return get_args(signature.return_annotation)
    return signature.return_annotation


def get_attributes_obj(obj: Callable) -> str:
    signature = inspect.signature(obj)
    return " ,".join(list(signature.parameters.keys()))


def is_optional(field: Any) -> Any:
    return get_origin(field) is Union and type(None) in get_args(field)


def validate_data_step(obj: Callable, additional_args: dict) -> None:
    """
    Validate provided data for execution step
    :param Callable obj: obj to execution
    :param additional_args: kwargs for execution obj
    :return: nothing
    :raises ExtraAttributeError: if in kwargs
    """
    signature_func = inspect.signature(obj)
    provided_args = set(additional_args.keys())
    existed_attributes = set(signature_func.parameters.keys())
    extra_attributes = provided_args - existed_attributes
    if extra_attributes and not is_exist_keyword_variable(obj):
        raise ExtraAttributeError(
            obj.__name__, list(additional_args), get_attributes_obj(obj)
        )


def is_exist_keyword_variable(obj: Callable) -> bool:
    """
    Check is exist **keyword variable in `obj`
    :param Callable obj: obj to execution
    :return: is exist in function **kwargs
    """
    for param in inspect.signature(obj).parameters.values():
        if str(param.kind) == "VAR_KEYWORD":
            return True
    return False


def validate_data_consistency(  # noqa: C901
    obj: Callable, return_previous_obj: Any, additional_args: dict
) -> None:
    """
    Function for validate data consistency between steps
    :param Callable obj: obj to execution
    :param return_previous_obj: annotations returned from previous step
    :param additional_args: kwargs for execution obj
    :return: nothing
    :raises DataConsistencyError: if not consistent data
    """
    signature_func = inspect.signature(obj)
    data_to_check = [return_previous_obj]
    if isinstance(return_previous_obj, tuple):
        data_to_check = list(return_previous_obj)
    if is_optional(return_previous_obj):
        # check is optional value
        for val in get_args(return_previous_obj):
            if val is not None:
                data_to_check = [val]
                break
    check_warnings = []
    errors = []

    for i, (param, val) in enumerate(signature_func.parameters.items()):
        # inspect._empty
        if i < len(data_to_check):
            # check in returned data
            if val.annotation != inspect._empty:  # type: ignore
                # check if the return type matches the expected type
                if data_to_check[i] == val.annotation:
                    continue  # pragma: no cover
                else:
                    errors.append(
                        "Expected and passed type do not match."
                        f" Expected `{val.annotation}`, passed `{data_to_check[i]}`"
                    )
            else:
                check_warnings.append(
                    f"Not exist annotations for variable `{param}`"
                )  # pragma: no cover
        else:
            # check in args or check is default
            if param in additional_args:
                # exist and we don't check type
                continue
            elif val.default != inspect._empty:  # type: ignore
                # not existing in additional_args but existing default value
                continue
            elif str(val.kind) == "VAR_KEYWORD":
                # for **kwargs
                continue
            else:
                # not returned, not existed in kwargs, not existing default value
                errors.append(
                    f"No value for variable `{param}`."
                    f" Provide a default value or pass a value when "
                    f"initializing the step"
                )
    if check_warnings:  # pragma: no cover
        warnings.warn(
            f"orch_serv.Stepper."
            f" Warnings in time check object `{obj.__name__}`. "
            f"Warning(s):\n {','.join(check_warnings)}",
            stacklevel=1,
        )
    if errors:
        raise DataConsistencyError(obj.__name__, errors)
