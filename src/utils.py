from pathlib import Path


def get_project_root():
    return Path(__file__).parent.parent


def from_project_root(path: str) -> str:
    return str(str(get_project_root()) + path)
