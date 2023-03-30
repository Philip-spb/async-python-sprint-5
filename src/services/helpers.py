from typing import Optional
from uuid import UUID


def parse_path(init_path: str) -> (str, Optional[str]):
    """
    init_path: <full-path-to-file>||<path-to-folder>
    """
    if init_path[0] == '/':
        init_path = init_path[1:]

    if init_path[-1] == '/':
        return init_path[:-1], None

    split_path = init_path.split('/')

    if len(split_path) == 1:
        return split_path[0], None

    path = '/'.join(split_path[:-1])
    return path, split_path[-1]


def is_uuid(path: str) -> bool:
    try:
        UUID(path)
    except ValueError:
        return False
    return True
