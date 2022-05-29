"""
Module with sync orchestrator
"""
import inspect
from logging import Logger
from types import ModuleType
from typing import Dict, List, Optional, Tuple, Type, Union

from orch_serv.exc import NoDateException, UniqueNameException, WrongTypeException
from orch_serv.msg import BaseOrchServMsg
from orch_serv.orchestrator.block import AsyncBlock, SyncBlock
from orch_serv.orchestrator.flow import AsyncFlow, SyncFlow
from orch_serv.settings import *  # noqa


class Orchestrator:
    """
    Orchestrator class for build service
    """

    _flows: Dict[
        str, Union[Type[Union[SyncFlow, AsyncFlow]], Union[SyncFlow, AsyncFlow]]
    ] = dict()
    _targets: Dict[
        str, Union[Type[Union[SyncBlock, AsyncBlock]], Union[SyncBlock, AsyncBlock]]
    ] = dict()

    def __init__(
        self,
        flows: Optional[Union[ModuleType, List]] = None,
        blocks: Optional[Union[ModuleType, List]] = None,
        logger: Optional[Logger] = None,
        flows_to_ignore: List[str] = None,
        blocks_to_ignore: List[str] = None,
    ):
        self.logger = logger or Logger(__name__)

        if flows:
            self._flows = self._generate_data(  # type: ignore
                data_to_process=flows,
                type_to_compare=(SyncFlow, AsyncFlow),
                attribute_to_get="name_flow",
                names_to_ignore=flows_to_ignore,
                type_data="flow",
            )
        if blocks:
            self._targets = self._generate_data(  # type: ignore
                data_to_process=blocks,
                type_to_compare=(SyncBlock, AsyncBlock),
                attribute_to_get="name_block",
                names_to_ignore=blocks_to_ignore,
                type_data="block",
            )
        if not self._targets and not self._flows:
            raise NoDateException(
                "orchestrator",
                "There is no data for the orchestrator to work correctly",
            )

    @staticmethod
    def _generate_data(
        data_to_process: Union[ModuleType, List],
        type_to_compare: Union[Type, Tuple[Type, ...]],
        attribute_to_get: str,
        names_to_ignore: Optional[List[str]] = list(),
        type_data: str = "block",
    ) -> Dict[str, Type[Union[SyncFlow, AsyncFlow, SyncBlock, AsyncBlock]]]:
        """
        The method prepares the data for the orchestrator to work
        Converts data from a list or retrieves from a module
        :param data_to_process:
        :param type_to_compare:
        :param attribute_to_get: name in object
        :param names_to_ignore: class names to ignore when processing
        :type names_to_ignore: List[str]
        :param type_data: name for information exception if will be raised
        :type type_data: str
        :raise TypeError: if the data to be processed contains
         the wrong type (and was not added to the exception)
        :raise UniqueNameException: if the data contains objects
         with non-unique identifiers
        :raise WrongTypeException: if a module is passed and
         not a list for generating data
        :raise NoDateException: if there is no data after processing
        :return: converted data to dictionary format to work with
        :rtype: Dict[str, Type[Union[Flow, SyncBlock, AsyncBlock]]]
        """
        _data = (
            dict()
        )  # type: Dict[str, Type[Union[SyncFlow, AsyncFlow, SyncBlock, AsyncBlock]]]
        if inspect.ismodule(data_to_process):
            for class_name, clazz in inspect.getmembers(
                data_to_process, inspect.isclass
            ):
                if class_name in names_to_ignore:
                    continue
                if not issubclass(clazz.__base__, type_to_compare):
                    raise TypeError(f"{type_data} is not inheritor {type_to_compare}")
                unique_identifier = getattr(clazz, attribute_to_get)
                if _data.get(unique_identifier):
                    raise UniqueNameException(unique_identifier, type_data)
                _data[unique_identifier] = clazz
        elif isinstance(data_to_process, list):
            for obj in data_to_process:
                if isinstance(obj, type):
                    if obj.__name__ in names_to_ignore:
                        continue
                    if issubclass(obj.__base__, type_to_compare):
                        unique_identifier = getattr(obj, attribute_to_get)
                        if _data.get(unique_identifier):
                            raise UniqueNameException(unique_identifier, type_data)
                        _data[unique_identifier] = obj
                    else:
                        raise TypeError(
                            f"{type_data}: `{obj}` is not inheritor {type_to_compare} "
                        )
                elif isinstance(obj, type_to_compare):
                    if obj.__class__.__name__ in names_to_ignore:
                        continue
                    unique_identifier = getattr(obj, attribute_to_get)
                    if _data.get(unique_identifier):
                        raise UniqueNameException(unique_identifier, type_data)
                    _data[unique_identifier] = obj
                else:
                    raise TypeError(
                        f"{type_data}: `{obj}` is not inheritor {type_to_compare} "
                    )

        else:
            raise WrongTypeException(type_data, str(type(data_to_process)))
        if not _data:
            raise NoDateException(type_data)
        return _data

    def handle(
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
                        target.process(message=message)
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
                        flow.to_go_with_the_flow(message=message)
                    except Exception as exc:
                        is_return_message = True
                        self.logger.warning(
                            "Orchestrator. Error processing msg %s in flow %s."
                            " Error: %s",
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