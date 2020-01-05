from discord.ext.commands import MemberConverter, UserConverter, NotOwner
import discord


async def get_discord_member(ctx, string):
    """
    Function used to get a member string if possible, if not a user string is returned. Otherwise it returns none.

    Parameters
    ----------
    ctx : discord.ext.commands.Context
        Represents the context in which a command is being invoked under.
    string : str
        Argument representing one of the elements needed for retrieving a discord user/member object

    Returns
    -------
    Member : discord.member.Member
        Returns a member object is the user element is found within the guild
    User : discord.user.User
        Returns a user object if the user element is not within the guild
    None :
        Returns None if the element was not able to be converted
    in_guild : bool
        True is member is in the guild "discord.member.Member"

    """
    # Attempting guild manual check
    for member in ctx.guild.members:
        if str(member.id) == str(string):
            return member, True
        elif member.name.lower() == string.lower():
            return member, True
        elif member.display_name.lower() == string.lower():
            return member, True
        elif f"{member.name}#{member.discriminator}".lower() == string.lower():
            return member, True

    # Try a global fetch
    try:
        global_member = await ctx.bot.fetch_user(string)
        if isinstance(global_member, discord.User):
            for member in ctx.guild.members:
                if member.id == global_member.id:
                    return member, True
            return global_member, False
    except:
        pass

    # Attempting global converter
    try:
        global_member = await UserConverter().convert(ctx, string)
        if isinstance(global_member, discord.User):
            for member in ctx.guild.members:
                if member.id == global_member.id:
                    return member, True
            return global_member, False
    except:
        return None, False

    # TODO: Add database check


def is_admin(ctx):
    """
    Simple check to see if the user invoking a command contains the elder role

    Parameters
    ----------
    ctx : discord.ext.commands.Context
        Represents the context in which a command is being invoked under.

    Returns
    -------
    bool:
        True or False if user is an elder
    """
    for role in ctx.author.roles:
        if role.id == 294283611870461953:
            return True
    return False


def is_owner(ctx):
    """
    Simple check to see if the user invoking a command is the owner

    Parameters
    ----------
    ctx : discord.ext.commands.Context
        Represents the context in which a command is being invoked under.

    Returns
    -------
    bool:
        True or False if user is an elder
    """
    if ctx.author.id == 265368254761926667:
        return True
    else:
        raise NotOwner("Not owner")


async def update_user(guild_member, update_dict):
    """
    Coro to update a users attributes from nickname to roles
    Parameters
    ----------
    guild_member : discord.member.Member
        Discord guild user object
    update_dict : dict
        Dictionary containing the items to change

    Raises
    ------
    discord.Forbidden
        Raised if the bot does not have the proper permissions or the roles of the target is higher than the bots

    """
    await guild_member.edit(nick=update_dict['nick'],
                            roles=role_list(guild_member, update_dict['roles']))


async def new_user_roles(ctx, player):
    """
    Coro users to return the two default roles every new user gets when they join the clan
    Parameters
    ----------
    ctx : discord.ext.commands.Context
        Represents the context in which a command is being invoked under.
    player : coc.SearchPlayer
        Clash player object

    Returns
    -------
    List of default roles

    """
    if player.town_hall not in ctx.bot.keys.static_roles:
        raise discord.InvalidData(f'Role `{player.town_hall}` does not exist. Create the role first.')
    zulu_server = ctx.bot.get_guild(ctx.bot.keys.zulu_server)
    town_hall_role_id = ctx.bot.keys.static_roles[player.town_hall]
    town_hall_role = zulu_server.get_role(town_hall_role_id)
    member_role = zulu_server.get_role(ctx.bot.keys.static_roles['coc_member'])
    return [town_hall_role, member_role]


def role_list(guild_member, new_roles):
    member_roles = guild_member.roles
    return member_roles.extend(new_roles)






