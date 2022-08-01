from typing import Any
from discord.ext import commands
from tabulate import tabulate
from datetime import datetime, timedelta
from pytz import timezone
from tabulate import tabulate
import time
import re
import discord

from discord import (ButtonStyle, Interaction, Member, SelectOption,
                     app_commands)
from discord.ui import Button, Modal, Select, TextInput, View
from utility.utils import defaultEmbed
from utility.paginators.GeneralPaginator import GeneralPaginator
from utility.apps.sekai.music_info import get_music, get_vocaloid_music, get_light_music_club_music, get_idol_music, get_street_music, get_theme_park_music, get_school_refusal_music


class SongCog(commands.Cog, name='song'):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    class SongView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.song_type = ''
            self.add_item(SongCog.SongSelect())

    class SongSelect(Select):
        def __init__(self):
            options = [SelectOption(label='虛擬歌手', description='バーチャル・シンガー', value='vocaloid'),
                       SelectOption(label='25點，Nightcord見。',
                                    description='25時、ナイトコードで。', value=1),
                       SelectOption(label='Leo/need',
                                    description='Leo/need', value=2),
                       SelectOption(label='MORE MORE JUMP！',
                                    description='MORE MORE JUMP！', value=3),
                       SelectOption(label='Vivid BAD SQUAD',
                                    description='Vivid BAD SQUAD', value=4),
                       SelectOption(label='Wonderlands×Showtime',
                                    description='ワンダーランズ×ショウタイム', value=5)
                       ]
            super().__init__(placeholder='選擇歌曲分類', options=options)
            
        async def callback(self, i: Interaction) -> Any:
            self.view: SongCog.SongView
            await i.response.defer()
            self.view.song_type = self.values[0]
            self.view.stop()

    @app_commands.command(name='songs', description='get songs info')
    async def song(self, i: Interaction):
        view = SongCog.SongView()
        await i.response.send_message(view=view)
        await view.wait()
        embeds = await get_music(self.bot.session, view.song_type)
        await GeneralPaginator(i, embeds).start(embeded=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SongCog(bot))
