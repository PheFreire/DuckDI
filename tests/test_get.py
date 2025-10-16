from unittest.mock import patch
from duckdi.modules.injections_container import InjectionsContainer
from duckdi.errors import InvalidAdapterImplementationError
from duckdi import Get, Interface, register
import pytest


def setup_function():
    InjectionsContainer.adapters.clear()
    InjectionsContainer.interfaces.clear()


def test_get_transient_instance():
    @Interface
    class IService: ...

    class Service(IService): ...

    register(Service)

    with patch(
        "duckdi.modules.injections_payload.InjectionsPayload.load",
        return_value={"i_service": "service"},
    ):
        resolved = Get(IService)
        assert isinstance(resolved, Service)


def test_get_singleton_instance():
    @Interface
    class IService: ...

    class Service(IService): ...

    register(Service, is_singleton=True)

    with patch(
        "duckdi.modules.injections_payload.InjectionsPayload.load",
        return_value={"i_service": "service"},
    ):
        resolved = Get(IService)
        assert resolved is InjectionsContainer.adapters["service"]


def test_get_invalid_adapter():
    @Interface
    class IService: ...

    class Invalid: ...

    InjectionsContainer.adapters["invalid"] = Invalid

    with patch(
        "duckdi.modules.injections_payload.InjectionsPayload.load",
        return_value={"i_service": "invalid"},
    ):
        with pytest.raises(InvalidAdapterImplementationError):
            Get(IService)


def test_get_service_by_label():
    @Interface(label="service")
    class IService:
        pass

    class Service(IService):
        pass

    register(Service, "adapter", is_singleton=True)

    with patch(
        "duckdi.modules.injections_payload.InjectionsPayload.load",
        return_value={"service": "adapter"},
    ):
        adapter = Get(IService, label="service")
        assert isinstance(adapter, Service)

def test_get_with_explicit_adapter_overrides_payload():
    @Interface
    class IRepository:
        pass

    class PostgresRepo(IRepository):
        pass

    class MemoryRepo(IRepository):
        pass

    register(PostgresRepo, "postgres_repo")
    register(MemoryRepo, "memory_repo")

    with patch(
        "duckdi.modules.injections_payload.InjectionsPayload.load",
        return_value={"i_repository": "postgres_repo"},
    ):
        resolved = Get(IRepository, adapter="memory_repo")
        assert isinstance(resolved, MemoryRepo)


def test_get_with_explicit_adapter_without_payload():
    @Interface
    class ILogger:
        pass

    class FileLogger(ILogger):
        pass

    register(FileLogger, "file_logger")

    with patch(
        "duckdi.modules.injections_payload.InjectionsPayload.load",
        return_value={},
    ):
        resolved = Get(ILogger, adapter="file_logger")
        assert isinstance(resolved, FileLogger)


def test_get_with_invalid_explicit_adapter_name():
    @Interface
    class IService:
        pass

    with patch(
        "duckdi.modules.injections_payload.InjectionsPayload.load",
        return_value={},
    ):
        with pytest.raises(KeyError):
            Get(IService, adapter="non_existent_adapter")


def test_get_with_explicit_adapter_not_implementing_interface():
    @Interface
    class IService:
        pass

    class WrongImpl:
        pass

    InjectionsContainer.adapters["wrong_impl"] = WrongImpl

    with patch(
        "duckdi.modules.injections_payload.InjectionsPayload.load",
        return_value={},
    ):
        with pytest.raises(InvalidAdapterImplementationError):
            Get(IService, adapter="wrong_impl")


def test_get_with_label_and_adapter_independent_behavior():
    @Interface(label="custom_service")
    class IService:
        pass

    class Service(IService):
        pass

    class AltService(IService):
        pass

    register(Service, "default_adapter")
    register(AltService, "alt_adapter")

    with patch(
        "duckdi.modules.injections_payload.InjectionsPayload.load",
        return_value={"custom_service": "default_adapter"},
    ):
        adapter = Get(IService, label="custom_service", adapter="alt_adapter")
        assert isinstance(adapter, AltService)

