from discord.ext.commands import MemberConverter, UserConverter


async def get_discord_member(ctx, object):
    # Attempting guild manual check
    for member in ctx.guild.members:
        if str(member.id) == str(object):
            return member
        elif member.name.lower() == object.lower():
            return member
        elif member.display_name.lower() == object.lower():
            return member
        elif f"{member.name}#{member.discriminator}".lower() == object.lower():
            return member

    # Attempting global converter
    user_converter = UserConverter()
    try:
        member = await user_converter.convert(ctx, object)
        return member
    except Exception as e:
        return None
