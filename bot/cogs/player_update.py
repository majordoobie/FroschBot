from datetime import datetime
from discord.ext import commands, tasks
import logging
from .utils.discord_arg_parser import arg_parser

# Local
from .utils.discord_arg_parser import arg_parser
from .utils.discord_utils import get_discord_member

class PlayerUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger('root.cogs.player_update')
        #self.update.start()

    @commands.command()
    async def _bot_status(self, ctx):
        await ctx.send('Database status: ')

    @commands.command(aliases=['add'])
    async def add_user(self, ctx, *, args=None):
        flag_template = {
            'clash_tag': {
                'flags': ['-t', '--tag'],
                'switch': False,
                'required': True
            },
            'guild_member': {
                'flags': ['-d', '--discord_id'],
                'switch': False,
                'required': True
            }
        }
        # Get parserd args
        parsed_args = await arg_parser(flag_template, args)

        result = await get_discord_member(ctx, parsed_args['guild_member'])
        #print(result)

        return
        # Get guild and global user object
        guild_member = ctx.author
        # global_member = await self.bot.fetch_user(guild_member.id)

        # Get times
        guild_join_date = guild_member.joined_at
        global_join_date = guild_member.created_at
        db_join_date = datetime.utcnow()

        # Get Names
        global_name = guild_member.name # TODO: Maybe use nick?
        guild_name = guild_member.display_name

        print(dir(global_name), dir(guild_name), guild_member.discriminator)
        return
        disc_member = ctx.author
        display_name = disc_member.display_name
        disc_name = disc_member.name
        disc_id = disc_member.id
        guild_joined = disc_member.joined_at
        global_user = await self.bot.fetch_user(disc_id)

        print(type(global_user))
        print(dir(global_user))
        print(dir(disc_name))

        return

        await ctx.send(parsed_args)
        discord_id = ctx.author.id
        print(discord_id)
        print('here')
        player = await self.bot.coc.get_player('#9P9PRYQJ')
        await ctx.send(f'Result: {player.name}')
        for i in dir(ctx.author):print(i)


def setup(bot):
    bot.add_cog(PlayerUpdate(bot))
