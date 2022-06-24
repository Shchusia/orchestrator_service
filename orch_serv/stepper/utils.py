import enum
import inspect
import warnings
from typing import Callable, Dict, Tuple, get_args, get_origin

from orch_serv.exc import DataConsistencyError, ExtraAttributeError


class ParameterKind(enum.IntEnum):
    POSITIONAL_ONLY = 0
    POSITIONAL_OR_KEYWORD = 1
    VAR_POSITIONAL = 2
    KEYWORD_ONLY = 3
    VAR_KEYWORD = 4


def format_signature_parameters(parameters) -> str:  # pragma: no cover
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
            render_pos_only_separator = True
        elif render_pos_only_separator:
            # It's not a positional-only parameter, and the flag
            # is set to 'True' (there were pos-only params before.)
            result.append("/")
            render_pos_only_separator = False

        if kind == ParameterKind.VAR_POSITIONAL.value:
            # OK, we have an '*args'-like parameter, so we won't need
            # a '*' to separate keyword-only arguments
            render_kw_only_separator = False
        elif kind == ParameterKind.KEYWORD_ONLY.value and render_kw_only_separator:
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
        result.append("/")

    return ", ".join(result)


def parse_signature(obj: Callable) -> Tuple[str, str]:
    """

    :param func:
    :return:
    """
    signature = inspect.signature(obj)
    return format_signature_parameters(signature.parameters), inspect.formatannotation(
        signature.return_annotation
    )


def get_returned_value(obj: Callable):
    signature = inspect.signature(obj)
    if get_origin(signature.return_annotation) == tuple:
        return get_args(signature.return_annotation)
    return signature.return_annotation


def get_attributes_obj(obj: Callable) -> str:
    signature = inspect.signature(obj)
    return " ,".join(list(signature.parameters.keys()))


def validation_data_consistency(
    obj: Callable, return_previous_obj, additional_args: Dict
):
    """

    :param obj:
    :param return_previous_obj:
    :param additional_args:
    :return: nothing
    :raises DataConsistencyError: if not consistent data
    """
    signature_func = inspect.signature(obj)
    # print(signature_func.parameters)
    data_to_check = [return_previous_obj]
    if isinstance(return_previous_obj, tuple):
        data_to_check = list(return_previous_obj)
    check_warnings = []
    errors = []
    for i, (param, val) in enumerate(signature_func.parameters.items()):
        # inspect._empty
        if i < len(data_to_check):
            # check in returned data
            if val.annotation != inspect._empty:  # type: ignore
                # check if the return type matches the expected type
                if data_to_check[i] == val.annotation:
                    if param in additional_args:
                        del additional_args[param]
                    continue
                else:
                    errors.append(
                        "Expected and passed type do not match."
                        f" Expected `{val.annotation}`, passed `{data_to_check[i]}`"
                    )
            else:
                check_warnings.append(f"Not exist annotations for variable `{param}`")
        else:
            # check in args or check is default
            if param in additional_args:
                # exist and we don't check type
                del additional_args[param]
                continue
            elif val.default != inspect._empty:  # type: ignore
                # not existing in additional_args but existing default value
                continue
            else:
                # not returned, not existed in kwargs, not existing default value
                errors.append(
                    f"No value for variable `{param}`."
                    f" Provide a default value or pass a value when "
                    f"initializing the step"
                )
    if additional_args:
        raise ExtraAttributeError(
            obj.__name__, list(additional_args), get_attributes_obj(obj)
        )
    if check_warnings:
        warnings.warn(
            f"orch_serv.Stepper."
            f" Warnings in time check object `{obj.__name__}`. "
            f"Warning(s):\n {','.join(check_warnings)}"
        )
    if errors:
        raise DataConsistencyError(obj.__name__, errors)
