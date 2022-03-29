"""
    I am not writing any more import-docstrings. these are pointless.
    """
from pathlib import Path
import json

# get_project_root() returns the root directory of the project as a Path-object.


def get_project_root():
    """Used to get the project folder path on any given harddrive. We do this to ensure that
    filepaths are always relative, which means that this bot should be able to run anywhere.

    Returns:
        Path: A Path-object
    """
    return Path(__file__).parent.parent


def from_project_root(path: str) -> str:
    """from_project_root(path) is supposed to be a simple way to navigate directories relative to
    the project root. Example: If your project root is '/home/user/this-project', calling
    'from_project_root('/config/token.txt')' returns '/home/user/this-project/config/token.txt'.

    Args:
        path (str): path to travel to. always assumes you are in the projects' main dir, because
        of get_project_root().

    Returns:
        str: an absolute path
    """
    return str(str(get_project_root()) + path)


def config_var(json_key: str):
    """config_var is used to easily retrieve key/values from config.json without having to do the
    full 'with open...' dance everytime.

    Args:
        json_key (str): the key which you want to retrieve the value from.

    Returns:
        any type: the value
    """
    with open(from_project_root('/config/config.json'), encoding='utf-8') as conf:
        __conf_dict__ = json.load(conf)
        return __conf_dict__[json_key]


def roles_var(json_key: str) -> int:
    """roles_var is used to easily retrieve key/values from roles.json without having to do the
    full 'with open...' dance everytime.

    Args:
        json_key (str): the key which you want to retrieve the value from.

    Returns:
        int: the id
    """
    with open(from_project_root('/config/roles.json'), encoding='utf-8') as role:
        __role_dict__ = json.load(role)
        return __role_dict__[json_key]
