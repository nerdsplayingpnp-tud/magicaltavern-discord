from pathlib import Path
import json

# get_project_root() returns the root directory of the project as a Path-object.


def get_project_root():
    return Path(__file__).parent.parent

# from_project_root(path) is supposed to be a simple way to navigate directories relative to the project root.
# Example: If your project root is '/home/user/this-project', calling 'from_project_root('/config/token.txt')'
# returns '/home/user/this-project/config/token.txt'.


def from_project_root(path: str) -> str:
    return str(str(get_project_root()) + path)


def config_var(json_key: str):
    with open(from_project_root('/config/config.json')) as conf:
        __conf_dict__ = json.load(conf)
        return __conf_dict__[json_key]
