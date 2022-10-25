import discord
from discord import app_commands, SelectOption
from discord.ext import commands
from discord.ui import (Select, 
                        View
)   

from data.emoji_data import group_icon_square
from data.img_data import group_icon
from utility.apps.sekai.music_info import get_group_music
from utility.utils import loadingEmbed
from utility.paginator import GeneralPaginator


class SongCog(commands.Cog, name='song'):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
                   
    @app_commands.command(name='songs', description='get songs info') 
    
    async def song(self, interaction: discord.Interaction): 
        select = Select(placeholder='選擇歌曲分類', options = [
                    SelectOption(label='25點，Nightcord見。', description='25時、ナイトコードで。', emoji= group_icon_square['school_refusal']), 
                    SelectOption(label='Leo/need', description='Leo/need', emoji= group_icon_square['light_music_club']), 
                    SelectOption(label='MORE MORE JUMP！', description='MORE MORE JUMP！', emoji= group_icon_square['idol']), 
                    SelectOption(label='Vivid BAD SQUAD', description='Vivid BAD SQUAD', emoji= group_icon_square['street']), 
                    SelectOption(label='Wonderlands×Showtime', description='ワンダーランズ×ショウタイム', emoji= group_icon_square['theme_park'])
                    ]) 
        
        async def song_callback(interaction: discord.Interaction):  
            
            await interaction.response.defer()
            global embed 
            embed = loadingEmbed(f' {select.values[0]} 的歌曲')
            
            if select.values[0] == '25點，Nightcord見。':
                await interaction.followup.send(embed=embed, ephemeral=True)
                embeds = await get_group_music('school_refusal', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
            if select.values[0] == 'Leo/need':
                await interaction.followup.send(embed=embed, ephemeral=True)
                embeds = await get_group_music('light_music_club', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
            if select.values[0] == 'MORE MORE JUMP！':
                await interaction.followup.send(embed=embed, ephemeral=True)
                embeds = await get_group_music('idol', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
            if select.values[0] == 'Vivid BAD SQUAD':
                await interaction.followup.send(embed=embed, ephemeral=True)
                embeds = await get_group_music('street', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
            if select.values[0] == 'Wonderlands×Showtime':
                await interaction.followup.send(embed=embed, ephemeral=True)
                embeds = await get_group_music('theme_park', self.bot.session)
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
        select.callback = song_callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message(view=view) 
              
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SongCog(bot))
