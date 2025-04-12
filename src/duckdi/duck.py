import os
from typing import Type
from os import getcwd, getenv

from duckdi.errors import InvalidAdapterImplementationError
from duckdi.utils import read_toml, to_snake


class __InjectionsBridge:
    """
    Internal structure that holds the mappings between registered interfaces and adapters.

    Attributes:
        adapters (dict): Maps the serialized interface name to its registered adapter class.
        interfaces (dict): Maps the serialized interface name to its interface class.
    """
    adapters = {}
    interfaces = {}

def __loadInjectionsPayload() -> dict[str, str]:
    """
    Loads the injection configuration from a TOML file defined by the INJECTIONS_PATH
    environment variable, or falls back to ./injections.toml.

    Returns:
        dict[str, str]: A dictionary mapping interface keys to adapter class names.

    Raises:
        FileNotFoundError: If the file does not exist.
        tomllib.TOMLDecodeError: If the file is not a valid TOML.
    """
    injections_path = getenv('INJECTIONS_PATH', os.path.join(getcwd(), 'injections.toml'))
    return read_toml(injections_path)["injections"]


def Interface[T](interface: Type[T]) -> Type[T]:
    """
    Registers an interface for dependency injection.

    Args:
        interface (Type[T]): The interface class to be registered.

    Returns:
        Type[T]: The same interface class, allowing usage as a decorator.

    Example:
        @Interface
        class IUserRepository: ...
    """
    __InjectionsBridge.interfaces[to_snake(interface)] = interface
    return interface


def register[T](adapter: Type[T]) -> None:
    """
    Registers an adapter (implementation) for a previously registered interface.

    Args:
        adapter (Type[T]): The concrete implementation class of a registered interface.

    Example:
        register(PostgresUserRepository)
    """
    __InjectionsBridge.adapters[to_snake(adapter)] = adapter


def Get[T](interface: Type[T]) -> T:
    """
    Resolves and returns an instance of the adapter associated with the given interface.

    Args:
        interface (Type[T]): The interface class annotated with @Interface.

    Returns:
        T: An instance of the adapter class bound to the interface.

    Raises:
        KeyError: If the interface or adapter is not properly registered or missing in the payload.
        InvalidAdapterImplementationError: If the resolved adapter does not implement the expected interface.

    Example:
        user_repo = Get(IUserRepository)
    """
    injections_payload = __loadInjectionsPayload()
    adapter = __InjectionsBridge.adapters[injections_payload[to_snake(interface)]]()

    if not isinstance(adapter, interface):
        raise InvalidAdapterImplementationError(interface.__name__, type(adapter).__name__)

    return adapter

