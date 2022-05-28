"""
Module consolidate all exceptions lib
"""


# pylint: disable=non-parent-init-called, super-init-not-called


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
