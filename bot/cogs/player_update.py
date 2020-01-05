from asyncpg import exceptions
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
        # self.update.start()

    @commands.check(utils.is_admin)
    @commands.command()
    async def _bot_status(self, ctx):
        await ctx.send('Database status: ')

    # @commands.check(utils.is_admin)
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

        # Change users nickname and add roles
        await self.bot.utils.update_user(ctx, disc_member, {'nick': player.name,
                                                            'roles': await self.bot.utils.new_user_roles(ctx, player)})


        # Get zbp status
        zbp_server = self.bot.get_guild(self.bot.keys.zbp_server)
        if disc_member in zbp_server.members:
            in_zbp = True
        else:
            in_zbp = False

        in_zulu_server = True
        is_active = True

        # Validate the user does not exist in the database
        async with self.bot.pool.acquire() as con:
            # Attempt to get user from db
            db_obj = await con.fetchrow('''
            SELECT * FROM discord_user WHERE discord_id=$1''', disc_member.id)

            # If user exists then we need to check if they are inactive or not
            if db_obj:
                if db_obj['is_active']:
                    # TODO: Check to see if there is an alt account to add
                    await ctx.send("User exists: Check to add new tag doe")
                else:
                    # TODO: Check to see if there is an alt account to add
                    await con.execute('''
                        UPDATE discord_user SET is_active = $1 WHERE discord_id = $2''',
                                      True, disc_member.id)
        print(db_obj)
        return

        # commit to discord_user
        user_data = [(
            disc_member.id,
            disc_member.name,
            disc_member.display_name,
            f"{disc_member.name}#{disc_member.discriminator}",
            disc_member.joined_at,
            disc_member.created_at,
            datetime.utcnow(),
            in_zbp,
            in_zulu_server,
            is_active
        ), ]
        async with self.bot.pool.acquire() as con:
            await con.copy_records_to_table('discord_user', records=user_data)
            await con.execute('''
                INSERT INTO clash_account VALUES ($1, $2, $3)
                ''', player.tag, disc_member.id, True)


def setup(bot):
    bot.add_cog(PlayerUpdate(bot))
