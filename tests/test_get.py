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

    # Registro com nome "adapter"
    register(Service, "adapter", is_singleton=True)

    # Mocka o carregamento da configuração de labels
    with patch(
        "duckdi.modules.injections_payload.InjectionsPayload.load",
        return_value={"service": "adapter"},
    ):
        adapter = Get(IService, label="service")
        assert isinstance(adapter, Service)

