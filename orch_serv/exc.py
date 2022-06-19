"""
Module consolidating all exceptions lib
"""

# pylint: disable=non-parent-init-called, super-init-not-called
from typing import List, Optional


class OrchServError(Exception):
    """
    Main exception class for custom exception lib
    """


class MsgException(OrchServError):
    """
    Main exception class for exceptions with msg
    """


class OrchestratorException(OrchServError):
    """
    Main exception class exceptions with Orchestrator
    """


class FlowException(OrchestratorException):
    """
    Error if the handler for the current message
     is not found in the flow
    """

    def __init__(self, message: str):
        self.message = (
            f"The flow chain ended without finding a single handler: {message}"
        )
        Exception.__init__(self, self.message)


class FlowBlockException(OrchestratorException):
    """
    Class custom exception
    for incorrect type of flow block
    """

    def __init__(self, message: str = ""):
        self.message = (
            f"Incorrect type block handler. "
            f"The block must inherit from the class 'Block',"
            f" and not : {message}"
        )
        Exception.__init__(self, self.message)


class FlowBuilderException(OrchestratorException):
    """
    Class custom exception
    for wrong types
    """

    def __init__(self, message: str = ""):
        self.message = f"Incorrect type in builder arguments {message}"
        Exception.__init__(self, self.message)


class UniqueNameException(OrchestratorException):
    """
    Exception for not unique flows
    """

    def __init__(self, not_unique_flow_name: str, _type: str):
        self.message = (
            f"The {_type} name `{not_unique_flow_name}` "
            f"is not unique to this orchestrator_service"
        )
        Exception.__init__(self, self.message)


class NoDateException(OrchestratorException):
    """
    Exception if dict flow is empty
    """

    def __init__(self, _type, msg: Optional[str] = None):
        if msg:
            self.message = msg
        else:
            self.message = f"No {_type}s for processing"
        Exception.__init__(self, self.message)


class WrongTypeException(OrchestratorException):
    """
    Exception for incorrect input types
    """

    def __init__(self, variable: str = "flows", type_variable: str = "any"):
        self.message = (
            f"Invalid variable type `{variable}`."
            f" There {variable} should be a list and not `{type_variable}`"
        )
        Exception.__init__(self, self.message)


class WorkTypeMismatchException(OrchestratorException):
    """
    if an asynchronous class is used for
     a synchronous orchestra, or vice versa
    """

    def __init__(self, base_class: str, obj_class: str, is_target: bool = False):
        self.message = (
            f"In {'targets' if is_target else 'flows'} use incorrect mode class."
            f"For {base_class} use {obj_class}."
            f" Different types of work (sync and async or vice versa)"
        )

        Exception.__init__(self, self.message)


class NotFoundDefaultError(OrchestratorException):
    """
    If provided default value but default value does not exist in processed data
    """

    def __init__(
        self, default_value: str, allowed_values: List[str], is_target: bool = False
    ):
        self.message = (
            f"Not exist default value {default_value}"
            f" for {'targets' if is_target else 'flows'}."
            f"Allowed values: {allowed_values}"
        )
        Exception.__init__(self, self.message)


class NotUniqueBlockInFlowError(OrchestratorException):
    """
    If provided default value but default value does not exist in processed data
    """

    def __init__(self, block_name: str, flow_name: str):
        self.message = (
            f"Not unique block {block_name}"
            f" in flow {flow_name}."
            f"Check your flow or set flow "
            f"`variable is_contains_duplicat_blocks` as True"
        )
        Exception.__init__(self, self.message)


class ServiceException(OrchServError):
    """
    Main exception class exceptions with Service
    """


class ServiceBlockException(ServiceException):
    """
    Class for exceptions in ServiceBlock
    """


class DoublePostProcessFunctionDeclaredError(ServiceException):
    """
    Exception if many default postprocess handlers
    """

    def __init__(self):
        self.message = "Several postprocessors specified"
        Exception.__init__(self, self.message)


class EmptyCommandsException(ServiceException):
    """
    Empty list of commands for service operation
    """

    def __init__(
        self,
    ):
        self.message = "Empty list of commands for service operation"
        Exception.__init__(self, self.message)


class NotUniqueCommandError(ServiceException):
    """
    Class error if user add the same commands
    """

    pass


class ServiceBuilderException(ServiceException):
    """
    Class for exceptions in BuilderService
    """

    pass


class IncorrectDefaultCommand(ServiceException):
    """
    Among the available commands, there is no default command
    """

    def __init__(self, command: str, list_command: List[str]):
        self.message = (
            f"The `{command}` command which is the default "
            f"command is not among the valid commands : {str(list_command)}"
        )
        Exception.__init__(self, self.message)
