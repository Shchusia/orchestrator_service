import pytest
from settings.settings_test_service import (
    CONST_LIST_ASYNC,
    CONST_LIST_SYNC,
    FirstAsyncPostProcessHandler,
    FirstAsyncProcessHandler,
    FirstPostProcessHandler,
    FirstProcessHandler,
    MyAsyncService,
    MySyncService,
    SecondAsyncPostProcessHandler,
    SecondAsyncProcessHandler,
    SecondPostProcessHandler,
    SecondProcessHandler,
    msg_to_async_first_handler,
    msg_to_async_forth_handler,
    msg_to_async_second_handler,
    msg_to_async_third_handler,
    msg_to_async_third_handler_with_error,
    msg_to_first_handler,
    msg_to_forth_handler,
    msg_to_second_handler,
    msg_to_third_handler,
    msg_to_third_handler_with_error,
)

from orch_serv.exc import (
    DoublePostProcessFunctionDeclaredError,
    EmptyCommandsException,
    IncorrectDefaultCommand,
    NotUniqueCommandError,
    ServiceBlockException,
    ServiceBuilderException,
)
from orch_serv.service import AsyncService, Service, ServiceBlock, ServiceBuilder


def test_setup_service():
    with pytest.raises(ServiceBuilderException):
        Service(service_commands=ServiceBlock)
    with pytest.raises(NotImplementedError):

        class MyService(Service):
            pass

        MyService()

    with pytest.raises(ServiceBuilderException):

        class MyService(Service):
            service_commands = ServiceBlock

        MyService()

    with pytest.raises(NotUniqueCommandError):

        class MyService(Service):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
                ServiceBlock(
                    processor=FirstProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
            )

        MyService()

    with pytest.raises(NotUniqueCommandError):

        class MyService(Service):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
                ServiceBlock(
                    processor=SecondProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
                ServiceBlock(
                    processor=FirstProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
            )

        MyService()

    with pytest.raises(IncorrectDefaultCommand):

        class MyService(Service):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
                ServiceBlock(
                    processor=SecondProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
            )

        MyService(default_command="test")
    with pytest.raises(TypeError):

        class MyService(Service):
            service_commands = ServiceBuilder(FirstProcessHandler)

    with pytest.raises(DoublePostProcessFunctionDeclaredError):

        class MyService(Service):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
                ServiceBlock(
                    processor=SecondProcessHandler,
                ),
                SecondPostProcessHandler(),
                default_post_process=SecondPostProcessHandler,
            )

    with pytest.raises(EmptyCommandsException):

        class MyService(Service):
            service_commands = ServiceBuilder(
                SecondPostProcessHandler(),
            )

    with pytest.raises(TypeError):

        class MyService(Service):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstAsyncProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
                default_post_process=SecondPostProcessHandler,
            )

        MyService()
    with pytest.raises(TypeError):

        class MyService(Service):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstProcessHandler,
                    post_processor=FirstAsyncPostProcessHandler,
                ),
                default_post_process=SecondPostProcessHandler,
            )

        MyService()
    with pytest.raises(ServiceBlockException):

        class MyService(Service):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstPostProcessHandler,
                    post_processor=FirstProcessHandler,
                ),
                default_post_process=SecondPostProcessHandler,
            )

        MyService()
    with pytest.raises(ServiceBlockException):

        class MyService(Service):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
                default_post_process=FirstProcessHandler,
            )

        MyService()


def test_setup_async_service():
    with pytest.raises(ServiceBuilderException):
        AsyncService(service_commands=ServiceBlock)
    with pytest.raises(NotImplementedError):

        class MyService(AsyncService):
            pass

        MyService()

    with pytest.raises(ServiceBuilderException):

        class MyService(AsyncService):
            service_commands = ServiceBlock

        MyService()

    with pytest.raises(NotUniqueCommandError):

        class MyService(AsyncService):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstAsyncProcessHandler,
                    post_processor=FirstAsyncPostProcessHandler,
                ),
                ServiceBlock(
                    processor=FirstAsyncProcessHandler,
                    post_processor=FirstAsyncPostProcessHandler,
                ),
            )

        MyService()

    with pytest.raises(NotUniqueCommandError):

        class MyService(AsyncService):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstAsyncProcessHandler,
                    post_processor=FirstAsyncPostProcessHandler,
                ),
                ServiceBlock(
                    processor=SecondAsyncProcessHandler,
                    post_processor=FirstAsyncPostProcessHandler,
                ),
                ServiceBlock(
                    processor=FirstAsyncProcessHandler,
                    post_processor=FirstAsyncPostProcessHandler,
                ),
            )

        MyService()

    with pytest.raises(IncorrectDefaultCommand):

        class MyService(AsyncService):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstAsyncProcessHandler,
                    post_processor=FirstAsyncPostProcessHandler,
                ),
                ServiceBlock(
                    processor=SecondAsyncProcessHandler,
                    post_processor=SecondAsyncPostProcessHandler,
                ),
            )

        MyService(default_command="test")
    with pytest.raises(TypeError):

        class MyService(AsyncService):
            service_commands = ServiceBuilder(FirstAsyncProcessHandler)

    with pytest.raises(DoublePostProcessFunctionDeclaredError):

        class MyService(AsyncService):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstAsyncProcessHandler,
                    post_processor=FirstAsyncPostProcessHandler,
                ),
                ServiceBlock(
                    processor=SecondAsyncProcessHandler,
                ),
                SecondAsyncPostProcessHandler(),
                default_post_process=SecondAsyncPostProcessHandler,
            )

    with pytest.raises(EmptyCommandsException):

        class MyService(AsyncService):
            service_commands = ServiceBuilder(
                SecondAsyncPostProcessHandler(),
            )

    with pytest.raises(TypeError):

        class MyService(AsyncService):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstProcessHandler,
                    post_processor=FirstAsyncPostProcessHandler,
                ),
                default_post_process=SecondAsyncPostProcessHandler,
            )

        MyService()
    with pytest.raises(TypeError):

        class MyService(AsyncService):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstAsyncProcessHandler,
                    post_processor=FirstPostProcessHandler,
                ),
                default_post_process=SecondAsyncPostProcessHandler,
            )

        MyService()
    with pytest.raises(ServiceBlockException):

        class MyService(AsyncService):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstAsyncPostProcessHandler,
                    post_processor=FirstAsyncProcessHandler,
                ),
                default_post_process=SecondAsyncPostProcessHandler,
            )

        MyService()
    with pytest.raises(ServiceBlockException):

        class MyService(AsyncService):
            service_commands = ServiceBuilder(
                ServiceBlock(
                    processor=FirstAsyncProcessHandler,
                    post_processor=FirstAsyncPostProcessHandler,
                ),
                default_post_process=FirstAsyncProcessHandler,
            )

        MyService()


def test_service_handler():
    CONST_LIST_SYNC.clear()
    service = MySyncService(is_catch_exceptions=True)
    res = service.handle(msg_to_first_handler)
    assert CONST_LIST_SYNC == [1, 4]
    assert res is None
    res = service.handle(msg_to_second_handler, is_force_return=True)
    assert CONST_LIST_SYNC == [1, 4, 2, 5]
    assert res == msg_to_second_handler
    service.handle(msg_to_third_handler)
    assert CONST_LIST_SYNC == [1, 4, 2, 5, 3]
    res = service.handle(msg_to_forth_handler)
    assert CONST_LIST_SYNC == [1, 4, 2, 5, 3]
    assert res == msg_to_forth_handler
    res = service.handle(msg_to_third_handler_with_error)
    assert CONST_LIST_SYNC == [1, 4, 2, 5, 3, 3]
    assert res == msg_to_third_handler_with_error

    service = MySyncService(
        default_command=FirstProcessHandler.target_command, is_catch_exceptions=False
    )
    res = service.handle(msg_to_forth_handler)
    assert CONST_LIST_SYNC == [1, 4, 2, 5, 3, 3, 1, 4]
    assert res is None
    with pytest.raises(ValueError):
        res = service.handle(msg_to_third_handler_with_error)
    assert CONST_LIST_SYNC == [1, 4, 2, 5, 3, 3, 1, 4, 3]


@pytest.mark.asyncio
async def test_async_service_handler():
    CONST_LIST_ASYNC.clear()
    service = MyAsyncService(is_catch_exceptions=True)
    res = await service.handle(msg_to_async_first_handler)
    assert CONST_LIST_ASYNC == [1, 4]
    assert res is None
    res = await service.handle(msg_to_async_second_handler, is_force_return=True)
    assert CONST_LIST_ASYNC == [1, 4, 2, 5]
    assert res == msg_to_async_second_handler
    await service.handle(msg_to_async_third_handler)
    assert CONST_LIST_ASYNC == [1, 4, 2, 5, 3]
    res = await service.handle(msg_to_async_forth_handler)
    assert CONST_LIST_ASYNC == [1, 4, 2, 5, 3]
    assert res == msg_to_async_forth_handler
    res = await service.handle(msg_to_async_third_handler_with_error)
    assert CONST_LIST_ASYNC == [1, 4, 2, 5, 3, 3]
    assert res == msg_to_async_third_handler_with_error

    service = MyAsyncService(
        default_command=FirstAsyncProcessHandler.target_command,
        is_catch_exceptions=False,
    )
    res = await service.handle(msg_to_async_forth_handler)
    assert CONST_LIST_ASYNC == [1, 4, 2, 5, 3, 3, 1, 4]
    assert res is None
    with pytest.raises(ValueError):
        res = await service.handle(msg_to_async_third_handler_with_error)
    assert CONST_LIST_ASYNC == [1, 4, 2, 5, 3, 3, 1, 4, 3]
