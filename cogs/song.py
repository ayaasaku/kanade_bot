from discord.ext import commands
from tabulate import tabulate
from datetime import datetime, timedelta
from pytz import timezone
from tabulate import tabulate
import time, re, discord

from discord import (ButtonStyle, Interaction, Member, SelectOption,
                     app_commands)
from discord.ui import Button, Modal, Select, TextInput
from utility.utils import defaultEmbed
from utility.paginators import GeneralPaginator
from utility.apps.sekai.music_info import get_group_music

class SongCog(commands.Cog, name='song'):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    class SelectOptions(Select):
        def __init__(self):
            options = [SelectOption(label='虛擬歌手', description='バーチャル・シンガー', value=0), 
                    SelectOption(label='25點，Nightcord見。', description='25時、ナイトコードで。', value=1), 
                    SelectOption(label='Leo/need', description='Leo/need', value=2), 
                    SelectOption(label='MORE MORE JUMP！', description='MORE MORE JUMP！', value=3), 
                    SelectOption(label='Vivid BAD SQUAD', description='Vivid BAD SQUAD', value=4), 
                    SelectOption(label='Wonderlands×Showtime', description='ワンダーランズ×ショウタイム', value=5)
                    ]
            super().__init__(placeholder='選擇歌曲分類', options=options)
            
    @app_commands.command(name='songs', description='get songs info')     
    async def song(self, i: discord.Interaction):  
        select_view = SongCog.SelectOptions()
        if self.SelectOptions.options == 0:
            embeds = await get_group_music('vocaloid', self.bot.session)
            await GeneralPaginator(i, embeds).start(embeded=True)
        elif self.SelectOptions.options == 1:
            embeds = await get_group_music('school_refusal', self.bot.session)
            await GeneralPaginator(i, embeds).start(embeded=True)
        elif self.SelectOptions.options == 2:
            embeds = await get_group_music('light_music_club', self.bot.session)
            await GeneralPaginator(i, embeds).start(embeded=True)
        elif self.SelectOptions.options == 3:
            embeds = await get_group_music('idol', self.bot.session)
            await GeneralPaginator(i, embeds).start(embeded=True) 
        elif self.SelectOptions.options == 4:
            embeds = await get_group_music('street', self.bot.session)
            await GeneralPaginator(i, embeds).start(embeded=True)
        elif self.SelectOptions.options == 5:
            embeds = await get_group_music('theme_park', self.bot.session)
            await GeneralPaginator(i, embeds).start(embeded=True)               
        return select_view
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SongCog(bot))
