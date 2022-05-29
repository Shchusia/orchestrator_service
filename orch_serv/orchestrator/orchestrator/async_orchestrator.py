"""
Module with async orchestrator
"""
from typing import Optional

from orch_serv.msg import BaseOrchServMsg

from .orchestrator import Orchestrator


class AsyncOrchestrator(Orchestrator):
    """
    AsyncOrchestrator
    override handle function for async mode
    """

    async def handle(  # type: ignore
        self, message: BaseOrchServMsg, is_force_return: bool = False
    ) -> Optional[BaseOrchServMsg]:
        """
        Message processing method

        !!! the presence of a `target` in the message is more priority
          than the presence of a `flow`
        :param message: message to process
        :type message: BaseOrchServMsg
        :param is_force_return: always return a message
        :type is_force_return: bool

        :return: message if an error occurred while processing the message
         if is_force_return is False
        :rtype: Optional[BaseOrchServMsg]
        """
        is_return_message = is_force_return
        self.logger.debug("Orchestrator. Started processing msg: %s", str(message))

        if message.get_flow() or message.get_target():
            if message.get_target():
                name_target = message.get_target()
                target = self._targets.get(name_target)
                if not target:
                    is_return_message = True
                    self.logger.warning(
                        "Orchestrator. No suitable target was found to process "
                        "this message with target: %s."
                        " Available targets: %s",
                        name_target,
                        list(self._targets.keys()),
                    )
                else:
                    if isinstance(target, type):
                        target = target(logger=self.logger)
                        self._targets[name_target] = target
                    try:
                        await target.process(message=message)
                    except Exception as exc:
                        is_return_message = True
                        self.logger.warning(
                            "Orchestrator. Error processing msg %s in target %s."
                            " Error: %s",
                            str(message),
                            name_target,
                            str(exc),
                            exc_info=True,
                        )
            else:
                name_flow = message.get_flow()
                flow = self._flows.get(name_flow)
                if not flow:
                    is_return_message = True
                    self.logger.warning(
                        "Orchestrator. No suitable flow was found to process "
                        "this message with flow: %s."
                        " Available flows: %s",
                        name_flow,
                        list(self._flows.keys()),
                    )
                else:
                    if isinstance(flow, type):
                        flow = flow(logger=self.logger)
                        self._flows[name_flow] = flow
                    try:
                        await flow.to_go_with_the_flow(message=message)
                    except Exception as exc:
                        is_return_message = True
                        self.logger.warning(
                            "Orchestrator. Error processing msg %s in flow %s. "
                            "Error: %s",
                            str(message),
                            name_flow,
                            str(exc),
                            exc_info=True,
                        )
        else:
            is_return_message = True
            self.logger.warning(
                "Orchestrator. Msg %s. "
                "Does not contain information about the type of"
                " processing and it was not processed",
                str(message),
            )
        self.logger.debug("Orchestrator. Finished processing msg: %s", str(message))
        if is_return_message:
            return message
        return None
