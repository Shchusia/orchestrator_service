"""
Module consolidate all exceptions lib
"""

# pylint: disable=non-parent-init-called, super-init-not-called
from typing import Optional


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
    for wrong type of flow block
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
    Exception for incorrect inputted types
    """

    def __init__(self, variable: str = "flows", type_variable: str = "any"):
        self.message = (
            f"Invalid variable type `{variable}`."
            f" There {variable} should be a list and not `{type_variable}`"
        )
