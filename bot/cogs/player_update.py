from discord.ext import commands, tasks


class PlayerUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.update.start()

    @commands.command()
    async def bot_status(self, ctx):
        await ctx.send('Database status: ')


def setup(bot):
    bot.add_cog(PlayerUpdate(bot))
