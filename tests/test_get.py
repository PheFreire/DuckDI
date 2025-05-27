from duckdi.injections.injections_container import InjectionsContainer
from duckdi.errors import InvalidAdapterImplementationError
from duckdi import Interface, register, Get
from unittest.mock import patch
import pytest

def setup_function():
    InjectionsContainer.adapters.clear()
    InjectionsContainer.interfaces.clear()

def test_get_transient_instance():
    @Interface
    class IService: ...
    class Service(IService): ...
    register(Service)

    with patch("duckdi.injections.injections_payload.InjectionsPayload.load", return_value={"i_service": "service"}):
        resolved = Get(IService)
        assert isinstance(resolved, Service)

def test_get_singleton_instance():
    @Interface
    class IService: ...
    class Service(IService): ...
    register(Service, is_singleton=True)

    with patch("duckdi.injections.injections_payload.InjectionsPayload.load", return_value={"i_service": "service"}):
        resolved = Get(IService)
        assert resolved is InjectionsContainer.adapters["service"]

def test_get_invalid_adapter():
    @Interface
    class IService: ...
    class Invalid: ...
    InjectionsContainer.adapters["invalid"] = Invalid

    with patch("duckdi.injections.injections_payload.InjectionsPayload.load", return_value={"i_service": "invalid"}):
        with pytest.raises(InvalidAdapterImplementationError):
            Get(IService)
