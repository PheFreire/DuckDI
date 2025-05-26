from duckdi.injections.injections_container import InjectionsContainer
from duckdi.errors import AdapterAlreadyRegisteredError
from duckdi import Interface, register
from typing import Protocol, runtime_checkable
import pytest

def setup_function():
    InjectionsContainer.adapters.clear()
    InjectionsContainer.interfaces.clear()

def test_register_transient_adapter():
    @Interface
    @runtime_checkable
    class IService(Protocol): ...
    class Service(IService): ...
    register(Service)
    assert "service" in InjectionsContainer.adapters

def test_register_singleton_adapter():
    @Interface
    @runtime_checkable
    class IService(Protocol): ...
    class Service(IService): ...
    register(Service, is_singleton=True)
    assert isinstance(InjectionsContainer.adapters["service"], Service)

def test_register_duplicate_adapter():
    @Interface
    @runtime_checkable
    class IService(Protocol): ...
    class Service(IService): ...
    register(Service)
    with pytest.raises(AdapterAlreadyRegisteredError):
        register(Service)
