import pytest

from duckdi import Interface
from duckdi.errors import InterfaceAlreadyRegisteredError
from duckdi.injections.injections_container import InjectionsContainer


def setup_function():
    InjectionsContainer.interfaces.clear()


def test_interface_registration():
    @Interface
    class IService: ...

    assert "i_service" in InjectionsContainer.interfaces


def test_interface_registration_duplicate():
    @Interface
    class IService: ...

    with pytest.raises(InterfaceAlreadyRegisteredError):

        @Interface
        class IService: ...
