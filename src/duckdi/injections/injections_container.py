from duckdi.errors import InvalidAdapterImplementationError, InterfaceAlreadyRegisteredError
from duckdi.errors.adapter_already_registered_error import AdapterAlreadyRegisteredError
from duckdi.injections.injections_payload import InjectionsPayload
from duckdi.utils import to_snake
from typing import Optional, Type

class __InjectionsContainer:
    """
    Internal structure that holds the mappings between registered interfaces and adapters.

    Attributes:
        adapters (dict): Maps the serialized interface name to its registered adapter class.
        interfaces (dict): Maps the serialized interface name to its interface class.
    """
    adapters = {}
    interfaces = {}


def Interface[T](interface: Type[T], label: Optional[str] = None) -> Type[T]:
    """
    Registers an interface for dependency injection.

    This function is used to declare an interface that can later be mapped to an adapter implementation.
    It ensures that the interface is uniquely registered under a resolved name or an optional label.

    Args:
        interface (Type[T]): The interface class to be registered.
        label (Optional[str]): An optional custom label for the interface. If not provided, a snake_case version
                               of the interface class name will be used.

    Returns:
        Type[T]: Returns the same interface class, enabling usage as a decorator.

    Raises:
        InterfaceAlreadyRegisteredError: If the interface or label has already been registered previously.

    Example:
        @Interface
        class IUserRepository:
            ...

        # or with a custom label
        @Interface(label="user_repo")
        class IUserRepository:
            ...
    """
    interface_name = label if label is not None else to_snake(interface)
    if __InjectionsContainer.interfaces.get(interface_name) is not None:
        raise InterfaceAlreadyRegisteredError(interface_name)
               
    __InjectionsContainer.interfaces[interface_name] = interface
    return interface


def register[T](adapter: Type[T], label: Optional[str] = None) -> None:
    """
    Registers an adapter (concrete implementation) for a previously registered interface.

    This function maps a class (adapter) to a name that can later be injected into services or providers.
    It prevents duplicate registrations to garantir consistência e evitar conflitos.

    Args:
        adapter (Type[T]): The concrete implementation class to register.
        label (Optional[str]): An optional custom label for the adapter. If not provided, a snake_case version
                               of the adapter class name will be used.

    Raises:
        AdapterAlreadyRegisteredError: If an adapter has already been registered under the same label.

    Example:
        register(PostgresUserRepository)

        # Or with custom label
        register(PostgresUserRepository, label="postgres_repo")
    """
    adapter_name = label if label is not None else to_snake(adapter)
    
    if __InjectionsContainer.adapters.get(adapter_name) is not None:
        raise AdapterAlreadyRegisteredError(adapter_name)

    __InjectionsContainer.adapters[adapter_name] = adapter


def Get[T](interface: Type[T], label: Optional[str] = None) -> T:
    """
    Resolves and returns an instance of the adapter associated with the given interface.

    This function is the main entry point for resolving dependencies no runtime.
    It uses the injection payload (geralmente definido em um arquivo `.toml`) para mapear a interface a um adaptador previamente registrado.

    Args:
        interface (Type[T]): The interface class decorated with @Interface.
        label (Optional[str]): Optional custom label used during interface registration. If omitted, the snake_case
                               name of the interface class is used.

    Returns:
        T: An instance of the adapter class bound to the interface.

    Raises:
        KeyError: If the interface is not found in the injection payload.
        InvalidAdapterImplementationError: If the resolved adapter does not implement the expected interface.

    Example:
        # Assuming IUserRepository was registered with @Interface
        # and PostgresUserRepository was registered with register(PostgresUserRepository)
        user_repo = Get(IUserRepository)
    """
    injections_payload = InjectionsPayload().load()
    interface_name = label if label is not None else to_snake(interface)
    adapter = __InjectionsContainer.adapters[injections_payload[interface_name]]()

    if not isinstance(adapter, interface):
        raise InvalidAdapterImplementationError(interface.__name__, type(adapter).__name__)

    return adapter


