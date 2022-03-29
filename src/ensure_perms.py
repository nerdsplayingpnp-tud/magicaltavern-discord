from itertools import Predicate
import discord
from discord.ext import commands
from helper_functions import roles_var

id_role_admin = roles_var('role-admin')
# Self gets passed because pylint wants it. i'm probably doing


def check_admin(ctx: commands.Context, self=None):
    # this wrong, but it cannot be that stupid if it works!
    """"check_admin() gets used as a predicate to check for all the possible conditions that
    would make a user an 'admin'-type user. The predicate returns True, if the Context User
    is either the bot owner, has the admin_role configured in
    config.json, or simply has administrator permissions.
    """
    def predicate(ctx):
        # ctx NEEDS to be passed to this predicate, because pycord demands it. The following
        # 2 lines are dedicated to remove a pylint warning.
        use_ctx = ctx
        ctx = use_ctx  # i hate this.
        return(commands.check_any(commands.has_role(id_role_admin),
                                  commands.has_permissions(
                                      administrator=True),
                                  commands.is_owner()))
    return commands.check(predicate)


def check_dungeonmaster(ctx: commands.Context, self=None):
    """"check_dungeonmaster() gets used as a predicate to check, if the user who called the command
    is equipped with the dungeon_master-role defined in roles.json. 
    The predicate returns True, if the Context User has the dungeon_master-role defined in
    roles.json"""
    def predicate(ctx):
        use_ctx = ctx
        ctx = use_ctx  # i hate this.
        return(commands.check_any(commands.has_role(roles_var('role-dm'))))
    return commands.check(predicate)
