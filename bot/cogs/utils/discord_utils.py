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
    Member : discord.Member
        Returns a member object is the user element is found within the guild
    User : discord.User
        Returns a user object if the user element is not within the guild
    None
        Returns None if the element was not able to be converted
    """
    # Attempting guild manual check
    for member in ctx.guild.members:
        if str(member.id) == str(string):
            return member
        elif member.name.lower() == string.lower():
            return member
        elif member.display_name.lower() == string.lower():
            return member
        elif f"{member.name}#{member.discriminator}".lower() == string.lower():
            return member

    # Try a global fetch
    try:
        member = await ctx.bot.fetch_user(string)
        if isinstance(member, discord.User):
            return member
    except:
        pass

    # Attempting global converter
    try:
        member = await UserConverter().convert(ctx, int(string))
        return member
    except Exception as e:
        return None

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
        #if role.id == 294283611870461953:
        if role.id == 493489002079322132:
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
    # TODO: DOn't forget to set real owner
    if ctx.author.id == 251150854571163648:
        return True
    else:
        raise NotOwner("Not owner")
    #return ctx.author.id == 251150854571163648 # 265368254761926667

