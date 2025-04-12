from typing import Type, TypeVar
from re import sub

T = TypeVar('T')

def to_snake(cls: Type[T]) -> str:
    return sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__.replace(" ", "_")).lower()
