import os
import sys
import traceback
from pathlib import Path

import aiohttp
import aiosqlite
import time

from discord import (Game, HTTPException, Intents, Interaction, Message,
                     Status, app_commands)
from discord.ext import commands, tasks
from dotenv import load_dotenv

from modules.debug import DebugView
from modules.main import errEmbed, log
#from utility.apps.sekai.virtual_live_info import virtual_live_ping_tw, virtual_live_ping_jp

load_dotenv()
token = os.getenv('TOKEN')
appid = os.getenv('APPID')
appsecret = os.getenv('APPSECRET')

intents = Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True
intents.presences = True

class KanadeBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=['!','%'],
            intents=intents,
            application_id=os.getenv('APP_ID')
        )
        
    async def setup_hook(self) -> None:
        self.repeat = False
        self.prev = False
        self.session = aiohttp.ClientSession()
        self.db = await aiosqlite.connect("kanade_data.db")
        self.backup_db = await aiosqlite.connect("backup.db")
        global version
        version = 2.1
        self.version = version
        
        await self.load_extension('jishaku')
        for filepath in Path('./cogs').glob('**/*.py'):
            cog_name = Path(filepath).stem
            await self.load_extension(f'cogs.{cog_name}')

    async def on_ready(self):
        await self.change_presence(
            status=Status.online,
            activity=Game(name=f'世界計畫')
        )
        print(log(True, False, 'Bot', f'Logged in as {self.user}'))

    async def on_message(self, message: Message):
        if message.author.id == self.user.id:
            return
        await self.process_commands(message)

    async def on_command_error(self, ctx, error) -> None:
        if hasattr(ctx.command, 'on_error'):
            return
        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return
        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except HTTPException:
                pass
        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)

    async def close(self) -> None:
        await self.session.close()
        return await super().close()


bot = KanadeBot()
tree = bot.tree


@tree.error
async def err_handle(i: Interaction, e: app_commands.AppCommandError):
    if isinstance(e, app_commands.errors.MissingRole):
        embed = errEmbed(message='你不是綾霞').set_author(
            name='權限不足', icon_url=i.user.avatar)
        if i.response._responded:
            await i.edit_original_message(embed=embed)
        else:
            await i.response.send_message(embed=embed, ephemeral=True)
    else:
        ayaakaa = i.client.get_user(831883841417248778)
        view = DebugView(traceback.format_exc())
        embed = errEmbed(message=f'```py\n{e}\n```').set_author(
            name='未知錯誤', icon_url=i.user.avatar)
        await i.channel.send(content=f'{ayaakaa.mention} 系統已將錯誤回報給綾霞, 請耐心等待修復', embed=embed, view=view)
   
@bot.listen()
async def on_ready():
    task_loop.start() 

    
@tasks.loop(seconds=1)
async def task_loop():
    pass
    #await virtual_live_ping_tw(bot, session)
    #await virtual_live_ping_jp(bot, session)


bot.run(token)


