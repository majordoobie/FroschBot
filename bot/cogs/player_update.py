from coc import utils as coc_utils
from datetime import datetime
from discord import member
from discord.ext import commands, tasks
import logging
from .utils.discord_arg_parser import arg_parser

# Local
from .utils.discord_arg_parser import arg_parser
from .utils import discord_utils as utils

class PlayerUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger('root.cogs.player_update')
        #self.update.start()

    @commands.check(utils.is_admin)
    @commands.command()
    async def _bot_status(self, ctx):
        await ctx.send('Database status: ')

    #@commands.check(utils.is_admin)
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

        # Attempt to find user
        disc_member, in_guild = await self.bot.utils.get_discord_member(ctx, parsed_args['guild_member'])
        if disc_member is None:
            await self.bot.embed_print(ctx, title='COMMAND ERROR', color='red',
                                       description=f"User `{parsed_args['guild_member']}` not found")
            return
        elif in_guild == False:
            await self.bot.embed_print(ctx, title='COMMAND ERROR', color='red',
                                       description=f"User `{disc_member.display_name}` is not in this guild")
            return

        # validate clash tag
        clash_tag = coc_utils.correct_tag(parsed_args['clash_tag'])
        try:
            player = await self.bot.coc.get_player(clash_tag)
        except:
            await self.bot.embed_print(ctx, title='CLASH ERROR', color='red',
                                       description=f'Player `{clash_tag}` not found')
            return

        # Change users nickname
        await self.bot.utils.update_user(disc_member, {'nick': player.name,
                                                       'roles': await self.bot.utils.new_user_roles(ctx, player)})

        return


        # Prepare to commit to database
        # Get names
        global_username = disc_member.name
        guild_nick = disc_member.nick       # Returns none if there is no nick
        global_discriminator = f"{disc_member.name}#{disc_member.discriminator}"


        # Get times
        guild_join_date = disc_member.joined_at
        global_join_date = disc_member.created_at
        database_join_date = datetime.utcnow()

        # Get zbp status
        zbp_server = self.bot.get_guild(self.bot.keys.zbp_server)
        if disc_member in zbp_server.members:
            in_zbp = True
        else:
            in_zbp = False


        print(player)
        print(clash_tag)
        return
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
