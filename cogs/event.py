import time, discord,asyncio
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from utility.utils import defaultEmbed
from data.emoji_data import attributes
from data.translate_data import translate
    
from utility.apps.sekai.time_formatting import format_time, format_date_jp, format_date, format_progress

from utility.apps.sekai.event_info import get_event_info_jp, get_event_info_tw
from utility.apps.sekai.user.profile import user_profile
from utility.apps.sekai.user.data_processing import *

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
                event_info = await get_event_info_jp(self.bot.session)
            elif option == 1:
                event_info = await get_event_info_tw(self.bot.session)
            event_id = event_info['event_id']
            event_end_time = event_info['event_end_time'] / 1000
            current_time = time.time()
            if current_time > event_end_time:
                await interaction.send("There's no active event!")
            else:
                if option == 0:
                    event_end_date = await format_date_jp(event_end_time * 1000)
                elif option == 1:
                    event_end_date = await format_date(event_end_time * 1000)    
                event_name = event_info['event_name']
                event_start_time = event_info['event_start_time']
                event_banner_name = event_info['event_banner_name']
                logo_url = f"https://minio.dnaroma.eu/sekai-assets/event/{event_banner_name}/logo_rip/logo.webp"
                banner_url = f"https://minio.dnaroma.eu/sekai-assets/home/banner/{event_banner_name}_rip/{event_banner_name}.webp"
                event_url = f'https://sekai.best/event/{event_id}'
                time_left = await format_time(event_end_time - current_time)
                event_prog = await format_progress(event_end_time, (event_start_time / 1000), current_time)
                embed = defaultEmbed(title=f'**{event_name}**')
                embed.set_thumbnail(url=logo_url)
                embed.set_image(url=banner_url)
                embed.add_field(name=f'剩餘時間', value=f'{time_left}', inline=False)
                embed.add_field(name=f'進度', value=f'{event_prog}', inline=False)
                embed.add_field(name=f'結束日期', value=f'{event_end_date}', inline=False)
                embed.add_field(name='更多資訊', value=event_url, inline=False)
                await interaction.response.send_message(embed=embed)
                
    @app_commands.command(name='event', description='查看本期活動的資訊')    
    @app_commands.rename(option='選項')
    @app_commands.choices(option=[
        Choice(name='jp', value=0),
        Choice(name='tw', value=1)])             
    async def event(self, interaction: discord.Interaction, option: int):      
        #jp
            global event_id
            if option == 0:
                event_info = await get_event_info_jp(self.bot.session)
            elif option == 1:
                event_info = await get_event_info_tw(self.bot.session)
            event_id = event_info['event_id']
            event_name = event_info['event_name']
            event_type = event_info['event_type']
            event_banner_name = event_info['event_banner_name']
            event_bonus_attribute = event_info['event_bonus_attribute']
            if option == 0:
                event_start_time = await format_date_jp(event_info['event_start_time'])
                event_end_time = await format_date_jp(event_info['event_end_time'])
            elif option == 1:
                event_start_time = await format_date(event_info['event_start_time'])
                event_end_time = await format_date(event_info['event_end_time'])
            logo_url = f"https://minio.dnaroma.eu/sekai-assets/event/{event_banner_name}/logo_rip/logo.webp"
            banner_url = f"https://minio.dnaroma.eu/sekai-assets/home/banner/{event_banner_name}_rip/{event_banner_name}.webp"
            event_url = f'https://sekai.best/event/{event_id}'
            event_attribute_translated = translate['attributes'][str(event_bonus_attribute)]
            attribute_emoji = attributes[str(event_bonus_attribute)]
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
            #embed.add_field(name='\u200b', value='**時間**', inline=False)
            embed.add_field(name='更多資訊', value=event_url, inline=False)
            await interaction.response.send_message(embed=embed)
            
    @app_commands.command(name='profile', description='查看一個玩家的帳戶')    
    #@app_commands.rename(user_id='玩家id')           
    async def profile(self, interaction: discord.Interaction):#, user_id: int): 
        #interaction.response.defer()
        user_id = 244775114281091084 
        if user_id == await get_user_game_data(user_id, 'userId', self.bot.session):
            name = await get_user_game_data(user_id, 'name', self.bot.session)
            id = user_id
            rank = await get_user_game_data(user_id, 'rank', self.bot.session)
            word = await get_user_profile(user_id, 'word', self.bot.session)
            twitter_id = await get_user_profile(user_id, 'twitterId', self.bot.session) 
            leader_id = await get_user_decks(user_id, 'leader', self.bot.session)
            img_url = await get_user_profile_pic(user_id, leader_id, self.bot.session)       
            
            embed = defaultEmbed(title=f'**{name}**', description=f'「{word}」')
            embed.set_thumbnail(url=img_url)
            embed.add_field(name=f'等級：', value=f'{rank}', inline=False)
            if twitter_id != None or len(twitter_id) >= 1: 
                embed.add_field(name=f'Twitter：', value=f'{twitter_id}', inline=False)
            embed.add_field(name=f'Id：', value=f'`{id}`', inline=False)
            
            #asyncio.sleep(0.01)
            interaction.response.send_message(embed=embed)
            #interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventCog(bot))
