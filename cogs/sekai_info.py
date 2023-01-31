import discord
from discord import app_commands, SelectOption
from discord.ui import (Select, View)   
from discord.ext import commands
from discord.app_commands import Choice


from modules.paginator import GeneralPaginator
from modules.main import loadingEmbed

from embeds.event import timeleft_embed, event_embed
from embeds.music import music_embed

from data.emoji_data import group_icon_square


class SekaiInfoCog(commands.Cog, name='sekai_info'):
    def __init__(self, bot):
        self.bot = bot


    #event    
    @app_commands.command(name='timeleft', description='查看本期活動的剩餘時間')
    @app_commands.rename(option='選項')
    @app_commands.choices(option=[
        Choice(name='jp', value='jp'),
        Choice(name='tw', value='tw')])  
    
    async def time_left(self, interaction: discord.Interaction, option: str):
        embed = await timeleft_embed(server=option)
        await interaction.response.send_message(embed=embed)
         
                
    @app_commands.command(name='event', description='查看本期活動的資訊')    
    @app_commands.rename(option='選項')
    @app_commands.choices(option=[
        Choice(name='jp', value='jp'),
        Choice(name='tw', value='tw')])   
             
    async def event(self, interaction: discord.Interaction, option: str):      
        embed = await event_embed(server=option)
        await interaction.response.send_message(embed=embed)
    
    #virtual_live 
    '''
    @app_commands.command(name='virtual_live', description='查看現正舉行的虛擬 Live')    
    @app_commands.rename(option='選項')
    @app_commands.choices(option=[
        Choice(name='jp', value=0),
        Choice(name='tw', value=1)])  
    async def virtual_live(self, interaction: discord.Interaction, option: int):  
        await interaction.response.defer() 
        if option == 0:
            embed = await get_current_virtual_live_embed('jp', self.bot.session)
        elif option == 1:
            embed = await get_current_virtual_live_embed('tw', self.bot.session)   
            
        if embed == None:
            embed = errEmbed('最近並沒有虛擬 Live 要舉行')
            await interaction.followup.send(embed=embed)
        else:
            if type(embed) is list:
                await GeneralPaginator(interaction, embed).start(embeded=True, follow_up=True)
            else:
                await interaction.followup.send(embed=embed)
    '''
    
    
    #music
    @app_commands.command(name='music', description='查看所有歌曲') 
    @app_commands.rename(option='選項')
    @app_commands.choices(option=[
        Choice(name='jp', value='jp'),
        Choice(name='tw', value='tw')])  
    
    async def music(self, interaction: discord.Interaction, option: str): 
        select = Select(placeholder='選擇歌曲分類', options = [
                    SelectOption(label='25點，Nightcord見。', description='25時、ナイトコードで。', emoji= group_icon_square['school_refusal']), 
                    SelectOption(label='Leo/need', description='Leo/need', emoji= group_icon_square['light_music_club']), 
                    SelectOption(label='MORE MORE JUMP！', description='MORE MORE JUMP！', emoji= group_icon_square['idol']), 
                    SelectOption(label='Vivid BAD SQUAD', description='Vivid BAD SQUAD', emoji= group_icon_square['street']), 
                    SelectOption(label='Wonderlands×Showtime', description='ワンダーランズ×ショウタイム', emoji= group_icon_square['theme_park'])
                    ]) 
        
        async def music_callback(interaction: discord.Interaction):   
            await interaction.response.defer()
            global embed 
            embed = loadingEmbed(f' {select.values[0]} 的歌曲')
            
            if select.values[0] == '25點，Nightcord見。':
                await interaction.followup.send(embed=embed, ephemeral=True)
                embeds = await music_embed(server=option, group='school_refusal')
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
            if select.values[0] == 'Leo/need':
                await interaction.followup.send(embed=embed, ephemeral=True)
                embeds = await music_embed(server=option, group='light_music_club')
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
            if select.values[0] == 'MORE MORE JUMP！':
                await interaction.followup.send(embed=embed, ephemeral=True)
                embeds = await music_embed(server=option, group='idol')
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
            if select.values[0] == 'Vivid BAD SQUAD':
                await interaction.followup.send(embed=embed, ephemeral=True)
                embeds = await music_embed(server=option, group='street')
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
            if select.values[0] == 'Wonderlands×Showtime':
                await interaction.followup.send(embed=embed, ephemeral=True)
                embeds = await music_embed(server=option, group='theme_park')
                await GeneralPaginator(interaction, embeds).start(embeded=True, follow_up=True)
                
        select.callback = music_callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message(view=view) 
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SekaiInfoCog(bot))