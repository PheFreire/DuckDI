from duckdi.injections.injections_container import InjectionsContainer
from duckdi.errors import InvalidAdapterImplementationError
from duckdi import Interface, register, Get
from unittest.mock import patch
from typing import Protocol, runtime_checkable
import pytest

def setup_function():
    InjectionsContainer.adapters.clear()
    InjectionsContainer.interfaces.clear()

@patch("duckdi.injections.injections_payload.InjectionsPayload.load", return_value={"i_service": "service"})
def test_get_transient_instance(mock_payload):
    @Interface
    @runtime_checkable
    class IService(Protocol): ...
    class Service(IService): ...
    register(Service)
    resolved = Get(IService)
    assert isinstance(resolved, Service)

@patch("duckdi.injections.injections_payload.InjectionsPayload.load", return_value={"i_service": "service"})
def test_get_singleton_instance(mock_payload):
    @Interface
    @runtime_checkable
    class IService(Protocol): ...
    class Service(IService): ...
    register(Service, is_singleton=True)
    resolved = Get(IService)
    assert resolved is InjectionsContainer.adapters["service"]

def test_get_invalid_adapter():
    @Interface
    @runtime_checkable
    class IService(Protocol): ...
    class Invalid: ...
    InjectionsContainer.adapters["invalid"] = Invalid
    with patch("duckdi.injections.injections_payload.InjectionsPayload.load", return_value={"i_service": "invalid"}):
        with pytest.raises(InvalidAdapterImplementationError):
            Get(IService)
