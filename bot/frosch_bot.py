# Built-in
import asyncio
import datetime
import logging
import traceback
import sys

# Non-built ins
from discord import Embed, Status, Game, HTTPException, InvalidData
from discord.errors import Forbidden
from discord.ext import commands
from cogs.utils import discord_utils
COG_PATH = 'cogs.'
COG_TUPLE = (
    'cogs.administrator',
    'cogs.player_update'
)
EMBED_COLORS = {
    'blue': 0x000080,       # info
    'red': 0xff0010,        # error
    'green': 0x00ff00       # success
}


class FroschBot(commands.Bot):
    __slots__ = ('bot_config', 'keys', 'bot_mode', 'log')

    def __init__(self, bot_config, keys, bot_mode, coc):
        self.bot_config = bot_config
        self.keys = keys
        self.bot_mode = bot_mode
        self.coc = coc
        self.cog_tupe = COG_TUPLE
        self.cog_path = COG_PATH
        self.utils = discord_utils
        self.debug = True
        super().__init__(command_prefix=self.bot_config['bot_prefix'])

        self.owner_id = keys.owner
        self.log = logging.getLogger('root.FroschBot')

    def run(self):
        print("Loading cogs...")
        for extension in COG_TUPLE:
            try:
                self.load_extension(extension)
            except Exception as e:
                out = f'Failed to load extension {extension}\n{e}'
                print(out)
                self.log.error(out)

        print('Cogs loaded - establishing connection...')
        super().run(self.bot_config['bot_token'], reconnect=True)

    # Connections
    async def on_resumed(self):
        self.log.info('Resumed connection from lost connection')

    async def on_ready(self):
        print("connected")
        self.log.info('Bot successfully logged on')
        await self.change_presence(status=Status.online, activity=Game(name=self.bot_config['version']))

    # Commands
    async def on_command(self, ctx):
        await ctx.message.channel.trigger_typing()

    async def on_command_error(self, ctx, error):
        if self.debug:
            exc = ''.join(
                traceback.format_exception(type(error), error, error.__traceback__, chain=True))
            await self.embed_print(ctx, title='DEBUG ENABLED', description=f'{exc}', codeblock=True)

        # Catch all errors within command logic
        if isinstance(error, commands.CommandInvokeError):
            original = error.original
            # Catch errors such as roles not found
            if isinstance(original, InvalidData):
                await self.embed_print(ctx, title='INVALID OPERATION', color='red',
                                       description=original.args[0])
                return

            # Catch permission issues
            elif isinstance(original, Forbidden):
                await self.embed_print(ctx, title='FORBIDDEN', color='red',
                                       description='Even with proper permissions, the target user must be lower in the '
                                       'role hierarchy of this bot.')
                return

        # Catch command.Check errors
        if isinstance(error, commands.CheckFailure):
            try:
                if error.args[0] == 'Not owner':
                    await self.embed_print(ctx, title='COMMAND FORBIDDEN', color='red',
                                           description='Only Doobie can run this command')
                    return
            except:
                pass
            await self.embed_print(ctx, title='COMMAND FORBIDDEN', color='red',
                                   description='Only `CoC Leadership` are permitted to use this command')
            return

        # Catch all
        await self.embed_print(ctx, title='COMMAND ERROR',
                               description=str(error), color='red')

    async def embed_print(self, ctx, title=None, description=None, color='blue', codeblock=False):
        """
        Method used to standardized how stuff is printed to the users
        Parameters
        ----------
        ctx
        title
        description
        color

        Returns
        -------

        """
        if len(description) < 1000:
            if codeblock:
                description = f'```{description}```'
            embed = Embed(
                title=f'__{title}__',
                description=description,
                color=EMBED_COLORS[color]
            )
            embed.set_footer(text=self.bot_config['version'])
            await ctx.send(embed=embed)
        else:
            blocks = await self.text_splitter(description, codeblock)
            embed_list = []
            embed_list.append(Embed(
                title=f'__{title}__',
                description=blocks[0],
                color=EMBED_COLORS[color]
            ))
            for i in blocks[1:]:
                embed_list.append(Embed(
                    description=i,
                    color=EMBED_COLORS[color]
                ))
            embed_list[-1].set_footer(text=self.bot_config['version'])
            for i in embed_list:
                await ctx.send(embed=i)

    async def text_splitter(self, text, codeblock):
        '''
        Method is used to split text by 1000 character increments to avoid hitting the
        1400 character limit on discord
        '''
        blocks = []
        block = ''
        for i in text.split('\n'):
            if (len(i) + len(block)) > 1000:
                block = block.rstrip('\n')
                if codeblock:
                    blocks.append(f'```{block}```')
                else:
                    blocks.append(block)
                block = f'{i}\n'
            else:
                block += f'{i}\n'
        if block:
            if codeblock:
                blocks.append(f'```{block}```')
            else:
                blocks.append(block)
        return blocks



