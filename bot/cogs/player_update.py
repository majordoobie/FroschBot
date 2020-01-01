from discord.ext import commands, tasks
import logging
from .utils.discord_arg_parser import arg_parser

# Local
from .utils.discord_arg_parser import arg_parser

class PlayerUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger('root.cogs.player_update')
        #self.update.start()

    @commands.command()
    async def _bot_status(self, ctx):
        await ctx.send('Database status: ')

    @commands.command(aliases=['add'])
    async def add_user(self, ctx, args=None):
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
        try:
            parsed_args = await arg_parser(flag_template, args)
        except Exception as e:
            print(dir(e.args))
            print('string',type(str(e)))
            print('traceback',e.with_traceback())
            await self.bot.embed_print(ctx, title='Command Line Error', color='red',
                                       description=str(e))
            print("did it work?")

        print(parsed_args)
        discord_id = ctx.author.id
        print(discord_id)
        print('here')
        player = await self.bot.coc.get_player('#9P9PRYQJ')
        await ctx.send(f'Result: {player.name}')


def setup(bot):
    bot.add_cog(PlayerUpdate(bot))
