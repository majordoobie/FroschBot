from discord.ext import commands, tasks
import logging
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
        discord_id = ctx.author.id
        print(discord_id)
        print('here')
        player = await self.bot.coc.get_player('#9P9PRYQJ')
        await ctx.send(f'Result: {player.name}')


def setup(bot):
    bot.add_cog(PlayerUpdate(bot))
