import getpass
import os
import sys
import traceback
from pathlib import Path

import aiohttp
import aiosqlite
from discord import (Game, HTTPException, Intents, Interaction, Message,
                     Status, app_commands)
from discord.ext import commands
from dotenv import load_dotenv
from pyppeteer import launch

from utility.utils import errEmbed

load_dotenv()
user_name = getpass.getuser()
if user_name == "alice":
    token = os.getenv('main')
    prefix = ['!', '！']
    guild = 778804551972159489
    application_id = 956049912699715634
    debug_toggle = False
else:
    token = os.getenv('dev')
    prefix = ['!']
    guild = 778804551972159489
    application_id = 957621570128449626
    debug_toggle = True

# 前綴, token, intents
intents = Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True
intents.presences = True


class KanadeBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = prefix,
            intents = intents,
            application_id = application_id,
            owner_ids = [289597294075183114,
                       410036441129943050, 831883841417248778]
        )

    async def on_ready(self):
        await self.change_presence(
            status=Status.online,
            activity=Game(name=f'/help',emoji=f'<:dot_dot_dot:1000044818166190140>')
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
        await self.db.close()
        await self.browser.close()
        await self.session.close()
        return await super().close()


bot = KanadeBot()
tree = bot.tree


@tree.error
async def err_handle(i: Interaction, e: app_commands.AppCommandError):
    if isinstance(e, app_commands.errors.MissingRole):
        embed = errEmbed(message='你不是小雪團隊的一員').set_author(
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

bot.run(token)

