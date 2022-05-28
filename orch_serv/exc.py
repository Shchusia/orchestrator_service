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
