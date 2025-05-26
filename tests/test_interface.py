from duckdi.injections.injections_container import InjectionsContainer
from duckdi.errors import InterfaceAlreadyRegisteredError
from duckdi import Interface
from typing import Protocol, runtime_checkable
import pytest

def setup_function():
    InjectionsContainer.interfaces.clear()

def test_interface_registration():
    @Interface
    @runtime_checkable
    class IService(Protocol): ...
    assert "i_service" in InjectionsContainer.interfaces

def test_interface_registration_duplicate():
    @Interface
    @runtime_checkable
    class IService(Protocol): ...

    with pytest.raises(InterfaceAlreadyRegisteredError):
        @Interface
        @runtime_checkable
        class IService(Protocol): ...
