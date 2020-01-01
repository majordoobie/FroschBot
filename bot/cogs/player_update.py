from discord.ext import commands, tasks
import logging
from .utils.utility import Utility


class PlayerUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.util = Utility(bot)
        self.log = logging.getLogger('root.cogs.player_update')
        #self.update.start()

    @commands.command()
    async def bot_status(self, ctx):
        await ctx.send('Database status: ')

    @commands.conmmand()
    async def add_user(self, ctx, args):
        pass

def setup(bot):
    bot.add_cog(PlayerUpdate(bot))
