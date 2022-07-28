from discord.ext import commands
from tabulate import tabulate
from datetime import datetime, timedelta
from pytz import timezone
from tabulate import tabulate
import time, re, discord

from discord import app_commands

from utility.utils import defaultEmbed


class SongCog(commands.Cog, name='song'):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='songs', description='get songs info')     
    @app_commands.rename(import_id='music_id')            
    async def event(self, interaction: discord.Interaction, import_id: int):
        from utility.apps.sekai.music_info import get_music_title, get_music_lyricist, get_music_composer, get_music_arranger,get_music_published_time, \
            get_music_difficulty_easy_difficulty, get_music_difficulty_easy_level, get_music_difficulty_easy_note_count, \
            get_music_difficulty_normal_difficulty, get_music_difficulty_normal_level, get_music_difficulty_normal_note_count, \
            get_music_difficulty_hard_difficulty, get_music_difficulty_hard_level, get_music_difficulty_hard_note_count, \
            get_music_difficulty_expert_difficulty, get_music_difficulty_expert_level, get_music_difficulty_expert_note_count, \
            get_music_difficulty_master_difficulty, get_music_difficulty_master_level, get_music_difficulty_master_note_count
        from utility.apps.sekai.time_formatting import format_date
        
        global music_id
        music_id = import_id
            
        music_title = await get_music_title(music_id)
        music_lyricist = await get_music_lyricist(music_id)
        music_composer = await get_music_composer(music_id)
        music_arranger = await get_music_arranger(music_id)
        music_published_time = await format_date(await get_music_published_time(music_id))
        if len(str(music_id)) == 1:
            music_asset_name = f'jacket_s_00{music_id}'
        elif len(str(music_id)) == 2:
            music_asset_name = f'jacket_s_0{music_id}'
        elif len(str(music_id)) == 3:
            music_asset_name = f'jacket_s_{music_id}'
            
        easy_difficulty = await get_music_difficulty_easy_difficulty(music_id)
        easy_level = await get_music_difficulty_easy_level(music_id)
        easy_note_count = await get_music_difficulty_easy_note_count(music_id)
        
        normal_difficulty = await get_music_difficulty_normal_difficulty(music_id)
        normal_level = await get_music_difficulty_normal_level(music_id)
        normal_note_count = await get_music_difficulty_normal_note_count(music_id)
        
        hard_difficulty = await get_music_difficulty_hard_difficulty(music_id)
        hard_level = await get_music_difficulty_hard_level(music_id)
        hard_note_count = await get_music_difficulty_hard_note_count(music_id)
        
        expert_difficulty = await get_music_difficulty_expert_difficulty(music_id)
        expert_level = await get_music_difficulty_expert_level(music_id)
        expert_note_count = await get_music_difficulty_expert_note_count(music_id)
        
        master_difficulty = await get_music_difficulty_master_difficulty(music_id)
        master_level = await get_music_difficulty_master_level(music_id)
        master_note_count = await get_music_difficulty_master_note_count(music_id)

        cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
        music_url = f'https://sekai.best/music/{music_id}'

        embed = defaultEmbed(title=f'**{music_title}**')
        embed.set_thumbnail(url=cover_url)
        embed.add_field(name='作詞', value=music_lyricist, inline=True)
        embed.add_field(name='作曲', value=music_composer, inline=True)
        embed.add_field(name='編曲', value=music_arranger, inline=True)
        embed.add_field(name='發佈時間', value=music_published_time, inline=False)
        embed.add_field(name='\u200b', value='**難度**', inline=False)
        embed.add_field(name=easy_difficulty, value=f'等級：{easy_level}\n音符數量：{easy_note_count}', inline=False)
        embed.add_field(name=normal_difficulty, value=f'等級：{normal_level}\n音符數量：{normal_note_count}', inline=True)
        embed.add_field(name=hard_difficulty, value=f'等級：{hard_level}\n音符數量：{hard_note_count}', inline=True)
        embed.add_field(name=expert_difficulty, value=f'等級：{expert_level}\n音符數量：{expert_note_count}', inline=False)
        embed.add_field(name=master_difficulty, value=f'等級：{master_level}\n音符數量：{master_note_count}\n\u200b', inline=True)
        embed.add_field(name='更多資訊', value=music_url, inline=False)
        #embed.add_field(name='\u200b', value='\u200b', inline=True)
        await interaction.response.send_message(embed=embed)
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SongCog(bot))
