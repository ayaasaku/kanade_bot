from discord.ext import commands
from tabulate import tabulate
from datetime import datetime, timedelta
from pytz import timezone
from tabulate import tabulate
import time, re, discord

from discord import (ButtonStyle, Interaction, Member, SelectOption,
                     app_commands)
from discord.ui import Button, Modal, Select, TextInput, View
from utility.utils import defaultEmbed
from utility.paginator import GeneralPaginator
from utility.apps.sekai.music_info import get_group_music

class SongCog(commands.Cog, name='song'):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
                   
    @app_commands.command(name='songs', description='get songs info') 
    
    async def song(self, interaction: discord.Interaction): 
        select = Select(placeholder='選擇歌曲分類', options = [SelectOption(label='虛擬歌手', description='バーチャル・シンガー'), 
                    SelectOption(label='25點，Nightcord見。', description='25時、ナイトコードで。'), 
                    SelectOption(label='Leo/need', description='Leo/need'), 
                    SelectOption(label='MORE MORE JUMP！', description='MORE MORE JUMP！'), 
                    SelectOption(label='Vivid BAD SQUAD', description='Vivid BAD SQUAD'), 
                    SelectOption(label='Wonderlands×Showtime', description='ワンダーランズ×ショウタイム')
                    ])
        
        async def song_callback(interaction: discord.Interaction):  
            await interaction.response.defer()
            if select.values[0] == '虛擬歌手':
                embeds = await get_group_music('vocaloid', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
            if select.values[0] == '25點，Nightcord見。':
                embeds = await get_group_music('school_refusal', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
            if select.values[0] == 'Leo/need':
                embeds = await get_group_music('light_music_club', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
            if select.values[0] == 'MORE MORE JUMP！':
                embeds = await get_group_music('idol', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
            if select.values[0] == 'Vivid BAD SQUAD':
                embeds = await get_group_music('street', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
            if select.values[0] == 'Wonderlands×Showtime':
                embeds = await get_group_music('theme_park', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
        select.callback = song_callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message(view=view) 
              
        
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SongCog(bot))