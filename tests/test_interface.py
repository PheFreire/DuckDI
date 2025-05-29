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


def test_interface_registration_with_label():
    @Interface(label="custom_label")
    class IFakeService:
        pass

    assert "custom_label" in InjectionsContainer.interfaces
    assert InjectionsContainer.interfaces["custom_label"] is IFakeService


def test_interface_duplicate_label_raises_error():
    @Interface(label="duplicate")
    class IFoo:
        pass

    with pytest.raises(InterfaceAlreadyRegisteredError):
        @Interface(label="duplicate")
        class IBar:
            pass
