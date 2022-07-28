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
        from utility.apps.sekai.music_info import get_music_title, get_music_lyricist, get_music_composer, get_music_arranger,get_music_published_time, get_music_asset_name
        from utility.apps.sekai.time_formatting import format_date
        
        global music_id
        music_id = import_id
            
        music_title = await get_music_title(music_id)
        music_lyricist = await get_music_lyricist(music_id)
        music_composer = await get_music_composer(music_id)
        music_arranger = await get_music_arranger(music_id)
        music_published_time = await format_date(await get_music_published_time(music_id))
        music_asset_name = get_music_asset_name(music_id)

        cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
        music_url = f'https://sekai.best/music/{music_id}'

        embed = defaultEmbed(title=f'**{music_title}**')
        embed.set_thumbnail(url=cover_url)
        embed.add_field(name='作詞', value=music_lyricist, inline=True)
        embed.add_field(name='作曲', value=music_composer, inline=True)
        embed.add_field(name='編曲', value=music_arranger, inline=True)
        embed.add_field(name='發佈時間', value=music_published_time, inline=False)
        embed.add_field(name='更多資訊', value=music_url, inline=False)
        #embed.add_field(name='\u200b', value='\u200b', inline=True)
        await interaction.response.send_message(embed=embed)
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SongCog(bot))
