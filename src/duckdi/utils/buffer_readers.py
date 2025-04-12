from src.duckdi.errors import MissingInjectionPayloadError
from os.path import isfile
from toml import load

def read_toml(path: str) -> dict[str, dict[str, str]]:
    if not isfile(path):
        raise MissingInjectionPayloadError(path)

    return load(open(buffer_path))



