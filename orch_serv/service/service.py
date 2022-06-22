"""
Module Service with help classes for build service
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from logging import Logger
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from pydantic import BaseModel

from orch_serv.exc import (
    DoublePostProcessFunctionDeclaredError,
    EmptyCommandsException,
    IncorrectDefaultCommand,
    NotUniqueCommandError,
    ServiceBlockException,
    ServiceBuilderException,
)
from orch_serv.msg import BaseOrchServMsg
from orch_serv.settings import DEFAULT_LOGGER


class CommandHandler(ABC):
    """
    Class with method for all handlers
    """

    _logger: Logger = DEFAULT_LOGGER  # for one global handler
    _service_instance: Service = None  # single scope for service_commands
    _is_logged = False

    @property
    def logger(self) -> Optional[Logger]:
        """
        get logger
        :return:  logger or None
        """
        return self._logger

    def set_logger(self, val: Any) -> None:
        """
        Set logger to handler
        :param Any val: logger
        :return: nothing
        :raise TypeError: if val is not a logger
        """
        if not val:
            return
        if isinstance(val, Logger):
            self._logger = val
        else:
            raise TypeError(f"Type must be logger but not {val}")

    def set_service_instance(self, service: Service) -> None:
        """
        set to instance handler current service object for use swap
        :param Service service:
        :return: nothing
        """
        if isinstance(service, Service):
            self._service_instance = service
        else:
            raise TypeError(f"Type must be Service but not {service}")

    def set_to_swap_scope(self, key: str, data: Any) -> bool:  # pragma: no cover
        """
        Method adds a value to the global scope for access from all services
        :param str key: name key
        :param Any data: data to add
        :return: bool: is_added_value
        """
        is_added = False
        if self._service_instance:
            try:
                setattr(self._service_instance, key, data)
                is_added = True
            except Exception as exc:
                if self.logger and self._is_logged:
                    self.logger.warning(
                        "Key `%s` not added. Error %s", key, str(exc), exc_info=True
                    )
        else:
            if self.logger and self._is_logged:
                self.logger.warning("You can't use swap because it is not initialized ")
        return is_added

    def get_from_swap_scope(self, key: str) -> Optional[Any]:  # pragma: no cover
        """
        Method gets a value available for all services from the global scope.
        :param str key: name key to get value
        :return: data if exist or None
        """
        data = None
        if self._service_instance:
            try:
                data = getattr(self._service_instance, key)
            except Exception as exc:
                if self.logger and self._is_logged:
                    self.logger.warning(
                        "Error while fetching data from swap by key %s. Error %s",
                        key,
                        str(exc),
                        exc_info=True,
                    )
        else:
            if self.logger and self._is_logged:
                self.logger.warning(
                    "You cann't use swap because it is not initialized "
                )
        return data

    def del_from_swap_scope(self, key: str) -> bool:  # pragma: no cover
        """
        Method removes attribute from swap_scope if any
        """
        is_dropped = False
        if self._service_instance:
            try:
                delattr(self._service_instance, key)
                is_dropped = True
            except Exception as exc:
                if self.logger and self._is_logged:
                    self.logger.warning(
                        "Key `%s` not deleted. Error %s", key, str(exc), exc_info=True
                    )
        else:
            if self.logger and self._is_logged:
                self.logger.warning("You can't use swap because it is not initialized ")
        return is_dropped


class CommandHandlerProcessStrategy(CommandHandler, ABC):
    """
    Handler class for base processing message
    """

    @property
    def target_command(self):  # pragma: no cover
        """
        this command will determine that the message should be processed
        by this particular service
        must be unique within the service
        """
        raise NotImplementedError

    @abstractmethod
    def process(
        self, msg: BaseOrchServMsg
    ) -> Union[Tuple[BaseOrchServMsg, Any], BaseOrchServMsg]:  # pragma: no cover
        """
        the main method for executing the logic of this handler, must be overridden
        in the inheritor
        :param MessageQueue msg: msg from queue
        :return: MessageQueue or None if return None post handler will not be called
        """
        raise NotImplementedError


class CommandHandlerPostProcessStrategy(CommandHandler, ABC):
    """
    Post Process Handler
    """

    @abstractmethod
    def post_process(
        self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None
    ) -> None:  # pragma: no cover
        """
        method for post-processing
        e.g. sending to another queue
        , must be overridden in the inheritor
        :param MessageQueue msg:
        :param additional_data: optional data got from processing block
        :return: None
        """
        raise NotImplementedError


class AsyncCommandHandlerProcessStrategy(CommandHandler, ABC):
    """
    Handler class for base processing message
    """

    @property
    def target_command(self):  # pragma: no cover
        """
        this command will determine that the message
        should be processed by this particular service
        must be unique within the service
        """
        raise NotImplementedError

    @abstractmethod
    async def process(
        self, msg: BaseOrchServMsg
    ) -> Union[Tuple[BaseOrchServMsg, Any], BaseOrchServMsg]:  # pragma: no cover
        """
        the main method for this handler execution logic, must be overridden
        in the inheritor
        :param MessageQueue msg: msg from queue
        :return: MessageQueue or None if return None post handler will not be called
        """
        raise NotImplementedError


class AsyncCommandHandlerPostProcessStrategy(CommandHandler, ABC):
    """
    Post Process Handler
    """

    @abstractmethod
    async def post_process(
        self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None
    ) -> None:  # pragma: no cover
        """
        method does post-processing
        e.g. sending to another queue
        , must be overridden in the inheritor
        :param MessageQueue msg:
        :param additional_data: optional data got from processing block
        :return: None
        """
        raise NotImplementedError


class DefaultPostProcessStrategy(CommandHandlerPostProcessStrategy):
    def post_process(self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None):
        """
        default post process function for sync service
        :param BaseOrchServMsg msg: msg received after processing
        :param Optional[Any] additional_data:
        :return: None
        """
        pass


class AsyncDefaultPostProcessStrategy(AsyncCommandHandlerPostProcessStrategy):
    async def post_process(
        self, msg: BaseOrchServMsg, additional_data: Optional[Any] = None
    ) -> None:
        """
        default post process function for async service
        :param BaseOrchServMsg msg: msg received after processing
        :param Optional[Any] additional_data:
        :return: None
        """
        pass


class ServiceCommand(BaseModel):
    """
    Structure class
    """

    processor: Union[CommandHandlerProcessStrategy, AsyncCommandHandlerProcessStrategy]
    post_processor: Union[
        CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy
    ]

    class Config:
        arbitrary_types_allowed = True


class ServiceBlock:
    """
    Class for build service - one Block with process
     and post process handlers
    """

    _processor: Union[
        CommandHandlerProcessStrategy, AsyncCommandHandlerProcessStrategy
    ] = None
    _post_processor: Optional[
        Union[CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy]
    ] = None

    @property
    def processor(
        self,
    ) -> Union[CommandHandlerProcessStrategy, AsyncCommandHandlerProcessStrategy]:
        """
        Property contains process handler
        :return: process command instance
        :rtype: Union[CommandHandlerProcessStrategy, AsyncCommandHandlerProcessStrategy]
        """
        return self._processor

    @property
    def post_processor(
        self,
    ) -> Union[
        CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy
    ]:
        """
        Property contains post_process handler
        :return: post_processor instance
        :rtype:Union[CommandHandlerPostProcessStrategy,
         AsyncCommandHandlerPostProcessStrategy]
        """
        return self._post_processor

    @processor.setter  # type: ignore # noqa
    def processor(  # noqa
        self,
        processor: Union[
            CommandHandlerProcessStrategy,
            AsyncCommandHandlerProcessStrategy,
            Type[CommandHandlerProcessStrategy],
            Type[AsyncCommandHandlerProcessStrategy],
        ],
    ) -> None:
        """
        Setups service processor and checks type
        :param processor:
        :raise ServiceBlockException:
        :return:
        """
        exc = ServiceBlockException(
            f"`process` object must be of type "
            f"`CommandHandlerProcessStrategy` or `AsyncCommandHandlerProcessStrategy` "
            f"and not {type(processor)}"
        )
        if isinstance(processor, type):
            if issubclass(
                processor,
                (CommandHandlerProcessStrategy, AsyncCommandHandlerProcessStrategy),
            ):
                self._processor = processor()
            else:
                raise exc
        elif isinstance(
            processor,
            (CommandHandlerProcessStrategy, AsyncCommandHandlerProcessStrategy),
        ):
            self._processor = processor
        else:
            raise exc

    @post_processor.setter  # type: ignore # noqa
    def post_processor(  # noqa
        self,
        post_processor: Optional[
            Union[
                CommandHandlerPostProcessStrategy,
                AsyncCommandHandlerPostProcessStrategy,
                Type[CommandHandlerPostProcessStrategy],
                Type[AsyncCommandHandlerPostProcessStrategy],
            ]
        ],
    ) -> None:
        """
        Setups service processor and checks type
        :param post_processor:
        :raise ServiceBlockException:
        :return:
        """
        if post_processor is None:
            return
        exc = ServiceBlockException(
            f"`post_processor` object must be of type "
            f"`CommandHandlerPostProcessStrategy` "
            f"or `AsyncCommandHandlerPostProcessStrategy`"
            f" and not {type(post_processor)}"
        )
        if isinstance(post_processor, type):
            if issubclass(
                post_processor,
                (
                    CommandHandlerPostProcessStrategy,
                    AsyncCommandHandlerPostProcessStrategy,
                ),
            ):
                self._post_processor = post_processor()
            else:
                raise exc
        elif isinstance(
            post_processor,
            (CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy),
        ):
            self._post_processor = post_processor
        else:
            raise exc

    def __init__(
        self,
        processor: Union[
            Type[CommandHandlerProcessStrategy],
            CommandHandlerProcessStrategy,
            Type[AsyncCommandHandlerProcessStrategy],
            AsyncCommandHandlerProcessStrategy,
        ],
        post_processor: Union[
            Type[CommandHandlerPostProcessStrategy],
            CommandHandlerPostProcessStrategy,
            Type[AsyncCommandHandlerPostProcessStrategy],
            AsyncCommandHandlerPostProcessStrategy,
        ] = None,
    ):
        """
        Init ServiceBlock
        :param CommandHandlerProcessStrategy process:
        :param CommandHandlerPostProcessStrategy post_process:
        """
        self.processor = processor  # type: ignore # noqa
        self.post_processor = post_processor  # type: ignore # noqa


class ServiceBuilder:
    """
    Class for aggregating service commands
    """

    _default_post_processor: Union[
        CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy
    ] = None

    @property
    def default_post_processor(
        self,
    ) -> Union[
        CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy
    ]:
        return self._default_post_processor

    @default_post_processor.setter
    def default_post_processor(
        self,
        default_post_processor: Union[
            CommandHandlerPostProcessStrategy,
            Type[CommandHandlerPostProcessStrategy],
            AsyncCommandHandlerPostProcessStrategy,
            Type[AsyncCommandHandlerPostProcessStrategy],
        ],
    ) -> None:
        """
        Setups service processor and checks correct type
        :param post_processor:
        :raise ServiceBlockException: if incorrect type
        :return:
        """
        if default_post_processor:
            message_error = (
                f"`default_post_processor` object must be of type "
                f"`CommandHandlerPostProcessStrategy` "
                f"and not {type(default_post_processor)}"
            )
            self._default_post_processor = self.check_is_post_processor(
                default_post_processor, message_error
            )

    @staticmethod
    def check_is_post_processor(obj: Any, message_error: str):
        """
        Method checks if obj is post_processor
        :param obj:
        :param message_error:
        :raise ServiceBlockException: if incorrect type

        :return:
        """
        exc = ServiceBlockException(message_error)
        if isinstance(obj, type):
            if issubclass(
                obj,
                (
                    CommandHandlerPostProcessStrategy,
                    AsyncCommandHandlerPostProcessStrategy,
                ),
            ):
                return obj()
            else:
                raise exc
        elif isinstance(
            obj,
            (CommandHandlerPostProcessStrategy, AsyncCommandHandlerPostProcessStrategy),
        ):
            return obj
        else:
            raise exc

    def __init__(
        self,
        *args: ServiceBlock,
        default_post_process: Optional[
            Union[
                Type[CommandHandlerPostProcessStrategy],
                CommandHandlerPostProcessStrategy,
                Type[AsyncCommandHandlerPostProcessStrategy],
                AsyncCommandHandlerPostProcessStrategy,
            ]
        ] = None,
    ):
        self.default_post_processor = default_post_process  # type: ignore # noqa
        list_blocks = list()  # type: List[ServiceBlock]
        for service_block in args:
            if isinstance(service_block, ServiceBlock):
                list_blocks.append(service_block)
            else:
                try:
                    post_processor = self.check_is_post_processor(service_block, "")
                    if self.default_post_processor:
                        raise DoublePostProcessFunctionDeclaredError()
                    else:
                        self.default_post_processor = post_processor
                except ServiceBlockException:
                    raise TypeError(
                        f"block must be instance class `ServiceBlock`."
                        f" Not {type(service_block)}"
                    )
        if not list_blocks:
            raise EmptyCommandsException()
        self._list_blocks = list_blocks

    def build(
        self, service_instance: Service, logger: Optional[Logger] = None
    ) -> Dict[str, ServiceCommand]:
        """
        Method builds all commands' current service.
        :param service_instance: current service
        :param Optional[Logger] logger: logger
        :return: {command_name: ServiceCommand} dict commands and proccess classes
        :rtype: Dict[str, ServiceCommand]
        """
        logger = logger or DEFAULT_LOGGER
        dict_commands = dict()  # type: Dict[str, ServiceCommand]

        if not self.default_post_processor:
            if service_instance._base_process_class == CommandHandlerProcessStrategy:
                self.default_post_processor = DefaultPostProcessStrategy()
            else:
                self.default_post_processor = AsyncDefaultPostProcessStrategy()

        self.default_post_processor.set_logger(logger)
        self.default_post_processor.set_service_instance(service_instance)

        for block in self._list_blocks:
            processor = block.processor
            post_processor = block.post_processor
            processor.set_logger(logger)  # noqa
            processor.set_service_instance(service_instance)
            if post_processor:
                post_processor.set_logger(logger)  # noqa
                post_processor.set_service_instance(service_instance)

            else:
                post_processor = self.default_post_processor

            if dict_commands.get(processor.target_command):
                raise NotUniqueCommandError(
                    f"Command `{processor.target_command}`"
                    f" is not unique for current service"
                )
            else:

                dict_commands[processor.target_command] = ServiceCommand(
                    processor=processor, post_processor=post_processor
                )
        return dict_commands


class Service(ABC):
    """
    Class Service for handle msg-s
    """

    _service_commands: ServiceBuilder = None
    _dict_handlers: Dict[str, ServiceCommand] = dict()
    _default_command: str = None
    _base_process_class = CommandHandlerProcessStrategy
    _base_post_process_class = CommandHandlerPostProcessStrategy

    def __init__(
        self,
        service_commands: Optional[ServiceBuilder] = None,
        default_command: Optional[str] = None,
        logger: Optional[Logger] = None,
        is_catch_exceptions: bool = True,
    ):
        self._is_catch_exceptions = is_catch_exceptions
        self.logger = logger or DEFAULT_LOGGER
        if not service_commands:
            # for validate if use property setup
            service_commands = self.service_commands

        self.__validate_service_builder(service_commands)
        self._dict_handlers = self.service_commands.build(
            service_instance=self, logger=logger
        )
        if default_command:
            if not self._dict_handlers.get(default_command):
                raise IncorrectDefaultCommand(
                    self._default_command, list(self._dict_handlers.keys())
                )
            else:
                self._default_command = default_command
        self._validate_data()

    def __validate_service_builder(self, service_builder: ServiceBuilder):
        """
        Help function for service_builder object validation
        :param service_builder:
        :return:
        """
        if not isinstance(service_builder, ServiceBuilder):
            raise ServiceBuilderException(
                f"Variable `service_builder` must be a"
                f" ServiceBuilder and not {type(service_builder)}"
            )
        self._service_commands = service_builder

    @property
    def service_commands(self) -> ServiceBuilder:  # pragma: no cover
        if not self._service_commands:
            raise NotImplementedError
        return self._service_commands

    @service_commands.setter
    def service_commands(self, service_builder: ServiceBuilder) -> None:
        self.__validate_service_builder(service_builder)

    def _validate_data(self):  # pragma: no cover
        """
        Help function to validate data service
        """
        if not issubclass(self._base_process_class, CommandHandler):
            raise TypeError(
                f"Incorrect type `_base_processor_class`. "
                f"Parent of variable `_base_processor_class` must be `CommandHandler`"
                f" and not {self._base_process_class.__base__}. "
                f"Please don`t override protected variable."
            )
        if not issubclass(self._base_post_process_class, CommandHandler):
            raise TypeError(
                f"Incorrect type `_base_post_processor_class`."
                f" Parent of variable `_base_post_processor_class` "
                f"must be `CommandHandler`"
                f" and not {self._base_post_process_class.__base__}. "
                f"Please don`t override protected variable."
            )
        for command_name, command in self._dict_handlers.items():
            if not isinstance(command.processor, self._base_process_class):
                raise TypeError(
                    f"Incorrect type `processor` of command `{command_name}`."
                    f" Must be a `{self._base_process_class.__name__}` "
                    f"and not `{command.processor.__class__.__base__.__name__}`"
                )
            if not isinstance(command.post_processor, self._base_post_process_class):
                raise TypeError(
                    f"Incorrect type `post_processor` of command `{command_name}`. "
                    f"Must be a `{self._base_post_process_class.__name__}` "
                    f"and not `{command.post_processor.__class__.__base__.__name__}`"
                )

    def _get_service_command(
        self, message: BaseOrchServMsg
    ) -> Optional[ServiceCommand]:
        """
        Function for get command to handle received message
        :param BaseOrchServMsg message: received message
        :return: handler if exist
        """
        command = self._dict_handlers.get(message.get_command())
        if command:
            return command
        elif self._default_command:
            return self._dict_handlers[self._default_command]
        else:
            return None

    def handle(
        self, message: BaseOrchServMsg, is_force_return: bool = False
    ) -> Optional[BaseOrchServMsg]:
        """
        the main function to process received messages
        :param BaseOrchServMsg message: message to process
        :param bool is_force_return: return msgs all time after execution
        :return: not processed msgs or received msgs if is_force_return==True
        """
        is_return_message = is_force_return
        self.logger.info("Service. Started processing message %s", message)
        command = self._get_service_command(message)
        if command:
            try:
                resp_process = command.processor.process(message)
                if resp_process:
                    try:
                        resp_msg, additional_data = resp_process  # type: ignore # noqa
                    except TypeError:
                        resp_msg, additional_data = resp_process, None
                    if command.post_processor and resp_msg:
                        command.post_processor.post_process(resp_msg, additional_data)
                else:
                    self.logger.debug(
                        "Don't send to post-processing because"
                        " processor doesn't return data."
                    )
            except Exception as exc:
                is_return_message = True
                self.logger.warning(
                    "Error in time processing msg %s. Error %s",
                    str(message),
                    str(exc),
                    exc_info=True,
                )
                if not self._is_catch_exceptions:
                    raise exc
        else:
            is_return_message = True
            self.logger.warning("Not found command to process message %s", str(message))

        self.logger.info("Service. Finished processing message %s", message)
        if is_return_message:
            return message
        return None


class AsyncService(Service, ABC):
    """ """

    _base_process_class = AsyncCommandHandlerProcessStrategy  # type: ignore # noqa
    _base_post_process_class = AsyncCommandHandlerPostProcessStrategy  # type: ignore # noqa

    async def handle(  # type: ignore # noqa
        self, message: BaseOrchServMsg, is_force_return: bool = False
    ) -> Optional[BaseOrchServMsg]:
        """

        :param message:
        :param is_force_return:
        :return:
        """
        is_return_message = is_force_return
        self.logger.info("Service. Started processing message %s", message)
        command = self._get_service_command(message)
        if command:
            try:
                resp_process = await command.processor.process(message)  # type: ignore # noqa
                if resp_process:
                    try:
                        resp_msg, additional_data = resp_process
                    except TypeError:
                        resp_msg, additional_data = resp_process, None
                    if command.post_processor and resp_msg:
                        await command.post_processor.post_process(
                            resp_msg, additional_data
                        )
                else:
                    self.logger.debug(
                        "Don't send to post-processing because "
                        "processor don't return data."
                    )
            except Exception as exc:
                is_return_message = True
                self.logger.warning(
                    "Error in time processing msg %s. Error %s",
                    str(message),
                    str(exc),
                    exc_info=True,
                )
                if not self._is_catch_exceptions:
                    raise exc
        else:
            is_return_message = True
            self.logger.warning("Not found command to process message %s", str(message))

        self.logger.info("Service. Finished processing message %s", message)
        if is_return_message:
            return message
        return None
