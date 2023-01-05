import time, discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from data.emoji_data import attributes
from data.translate_data import translate
    
from utility.apps.sekai.time_formatting import format_time, format_date_jp, format_date, format_progress
from utility.apps.sekai.event_info import get_event_info
from utility.apps.sekai.virtual_live_info import get_current_virtual_live_embed
from utility.apps.sekai.user.data_processing import *

from utility.utils import defaultEmbed, errEmbed
from utility.paginator import GeneralPaginator


class EventCog(commands.Cog, name='event'):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='timeleft', description='查看本期活動的剩餘時間')
    @app_commands.rename(option='選項')
    @app_commands.choices(option=[
        Choice(name='jp', value=0),
        Choice(name='tw', value=1)])  

    async def time_left(self, interaction: discord.Interaction, option: int):
            if option == 0:
                event_info = await get_event_info(self.bot.session, 'jp')
            elif option == 1:
                event_info = await get_event_info(self.bot.session, 'tw')
                
            if event_info == None:
                await interaction.response.send_message(embed = errEmbed('現時並沒有舉行任何活動'))
            else:
                current_time = int(time.time())   
                event_id = event_info['event_id']
                event_end_time = event_info['event_end_time']
                event_name = event_info['event_name']
                event_start_time = event_info['event_start_time']
                event_banner_name = event_info['event_banner_name']
                if option == 0: #jp
                    event_end_date = await format_date_jp(event_end_time)
                    logo_url = f"https://storage.sekai.best/sekai-assets/event/{event_banner_name}/logo_rip/logo.webp"
                    banner_url = f"https://storage.sekai.best/sekai-assets/home/banner/{event_banner_name}_rip/{event_banner_name}.webp"
                elif option == 1: #tw
                    event_end_date = await format_date(event_end_time)   
                    logo_url = f"https://storage.sekai.best/sekai-tc-assets/event/{event_banner_name}/logo_rip/logo.webp"
                    banner_url = f"https://storage.sekai.best/sekai-tc-assets/home/banner/{event_banner_name}_rip/{event_banner_name}.webp"
                event_url = f'https://sekai.best/event/{event_id}'
                time_left = await format_time(event_end_time - current_time)
                event_progress = await format_progress(event_end_time, event_start_time, current_time)
                
                embed = defaultEmbed(title=f'**{event_name}**')
                embed.set_thumbnail(url=logo_url)
                embed.set_image(url=banner_url)
                embed.add_field(name=f'剩餘時間', value=f'{time_left}', inline=False)
                embed.add_field(name=f'進度', value=f'{event_progress}', inline=False)
                embed.add_field(name=f'結束日期', value=f'{event_end_date}', inline=False)
                embed.add_field(name='更多資訊', value=event_url, inline=False)
                
                await interaction.response.send_message(embed=embed)
                
    @app_commands.command(name='event', description='查看本期活動的資訊')    
    @app_commands.rename(option='選項')
    @app_commands.choices(option=[
        Choice(name='jp', value=0),
        Choice(name='tw', value=1)])  
               
    async def event(self, interaction: discord.Interaction, option: int):      
        global event_id
        
        if option == 0:
            event_info = await get_event_info(self.bot.session, 'jp')
        elif option == 1:
            event_info = await get_event_info(self.bot.session, 'tw')
            
        if event_info == None:
            await interaction.response.send_message(embed = errEmbed('現時並沒有舉行任何活動'))
            
        else:
            event_id = event_info['event_id']
            event_name = event_info['event_name']
            event_type = event_info['event_type']
            event_banner_name = event_info['event_banner_name']
            event_bonus_attribute = event_info['event_bonus_attribute']
            
            if option == 0:
                event_start_time = await format_date_jp(event_info['event_start_time'])
                event_end_time = await format_date_jp(event_info['event_end_time'])
                logo_url = f"https://storage.sekai.best/sekai-assets/event/{event_banner_name}/logo_rip/logo.webp"
                banner_url = f"https://storage.sekai.best/sekai-assets/home/banner/{event_banner_name}_rip/{event_banner_name}.webp"
            elif option == 1:
                event_start_time = await format_date(event_info['event_start_time'])
                event_end_time = await format_date(event_info['event_end_time'])
                logo_url = f"https://storage.sekai.best/sekai-tc-assets/event/{event_banner_name}/logo_rip/logo.webp"
                banner_url = f"https://storage.sekai.best/sekai-tc-assets/home/banner/{event_banner_name}_rip/{event_banner_name}.webp"
                
            event_url = f'https://sekai.best/event/{event_id}'
            attribute_emoji = attributes[str(event_bonus_attribute)]
            event_attribute_translated = translate['attributes'][str(event_bonus_attribute)]
            event_type_translated = translate['event_type'][str(event_type)]
            event_bonus_characters_name_list = event_info['characters_name_list']
            
            embed = defaultEmbed(title=f'**{event_name}**')
            embed.set_thumbnail(url=logo_url)
            embed.set_image(url=banner_url)
            embed.add_field(name='活動類型', value=event_type_translated, inline=False)  
            embed.add_field(name='加成屬性', value=f'{attribute_emoji} {event_bonus_attribute}\n({event_attribute_translated})', inline=True)
            embed.add_field(name='\u200b', value='\u200b', inline=True)
            
            if len(event_bonus_characters_name_list) == 1:
                embed.add_field(name='加成角色', value=f'{event_bonus_characters_name_list[0]}', inline=True)  
            elif len(event_bonus_characters_name_list) == 2:
                embed.add_field(name='加成角色', value=f'{event_bonus_characters_name_list[0]}，{event_bonus_characters_name_list[1]}', inline=True)      
            elif len(event_bonus_characters_name_list) == 3:
                embed.add_field(name='加成角色', value=f'{event_bonus_characters_name_list[0]}，{event_bonus_characters_name_list[1]}\n{event_bonus_characters_name_list[2]}', inline=True)      
            elif len(event_bonus_characters_name_list) == 4:
                embed.add_field(name='加成角色', value=f'{event_bonus_characters_name_list[0]}，{event_bonus_characters_name_list[1]}\n{event_bonus_characters_name_list[2]}，{event_bonus_characters_name_list[3]}', inline=True)  
                    
            embed.add_field(name='開始', value=event_start_time, inline=True)
            embed.add_field(name='\u200b', value='\u200b', inline=True)
            embed.add_field(name='結束', value=f'{event_end_time}', inline=True)
            embed.add_field(name='更多資訊', value=event_url, inline=False)
            
            await interaction.response.send_message(embed=embed)
        
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
            
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventCog(bot))