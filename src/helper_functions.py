from pathlib import Path
import json

# get_project_root() returns the root directory of the project as a Path-object.
import discord


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


def roles_var(json_key: str):
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


def user_has_role_id(ctx: discord.Interaction, role_id: int) -> bool:  #TODO: Rename this or re-implement this. The name
    # TODO: of the function is misleading.
    """
    Method that checks if a user from a command interaction has a specific role. Returns True if the
    user has the specified role id.
    @param ctx: Discord Interaction Context
    @param role_id: The role id to check against.
    """
    role_check = False
    for i in ctx.user.roles:
        if roles_var('role-dm') == i.id:
            role_check = True
    return role_check


def user_has_any_role(ctx: discord.Interaction, role_ids: [int]) -> bool:
    """
    Method that checks if a user from a command interaction has any of the given roles. Returns True if the user has
    any of the specified role ids.
    @param ctx: Discord Interaction Context
    @param role_ids: The role ids to check against.
    """
    roles_check = False
    for i in ctx.user.roles:
        for j in role_ids:
            if i.id == j:
                roles_check = True
    return roles_check
