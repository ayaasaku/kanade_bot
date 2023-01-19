import aiosqlite

import discord
from discord import Embed, app_commands, ui, SelectOption
from discord.ui import View, Select
from discord.ext import commands
from discord.app_commands import Choice
from matplotlib.pyplot import get

from modules.main import defaultEmbed, loadingEmbed, errEmbed, successEmbed, is_ayaakaa,notAyaakaaEmbed
from modules.paginator import GeneralPaginator

from embeds.profile import user_profile_embed

from data.emoji_data import *

class SekaiProfileCog(commands.Cog, name='sekai_profile'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        global none_embed
        none_embed = errEmbed(
            '玩家ID不存在',
            f'也許該名玩家還沒注冊？\n可以使用 `/register` 來註冊') 
    
    @app_commands.command(name='profile', description='查看一個玩家的帳戶') 
    @app_commands.rename(person='其他玩家')
    @app_commands.choices(option=[
        Choice(name='jp', value='jp'),
        Choice(name='tw', value='tw')])  
    async def profile(self, interaction: discord.Interaction, option:str, person: discord.User = None):
        await interaction.response.defer(ephemeral=True)
        if option == 'tw':
            embed = errEmbed(
            '目前還沒支持台服喔',
            f'台服的功能將於稍後推出，\n敬請期待。') 
            interaction.followup.send(embed=embed) 
        else:
            db = await aiosqlite.connect("kanade_data.db")
            cursor = await db.cursor()
            if person == None:
                discord_id = interaction.user.id
                person = interaction.user
            else:
                discord_id = person.id   
            await cursor.execute('SELECT player_id from user_accounts WHERE discord_id = ?', (str(discord_id),))
            player_id = await cursor.fetchone()
            if player_id is None:
                embed = none_embed
                await interaction.followup.send(embed=embed, ephemeral= True)
            else:
                player_id = player_id[0]
                if type(player_id) != str: str(player_id)
                loading_embed = loadingEmbed(text = '玩家')
                await interaction.followup.send(embed=loading_embed)
                embed_list = await user_profile_embed(import_id=player_id, server=option)
                embed_list[0].set_author(name=person.display_name, icon_url= person.display_avatar)
                await GeneralPaginator(interaction, embed_list).start(embeded=True, follow_up=True)
    
    '''     
    @app_commands.command(name='area-items', description='查看一個玩家的區域道具') 
    @app_commands.rename(person='其他玩家')
    async def area_items(self, interaction: discord.Interaction, person: discord.User = None):
        await interaction.response.defer(ephemeral=True)
        db = await aiosqlite.connect("kanade_data.db")
        cursor = await db.cursor()
        if person == None:
            discord_id = interaction.user.id
            person = interaction.user
        else:
            discord_id = person.id
        await cursor.execute('SELECT player_id from user_accounts WHERE discord_id = ?', (str(discord_id),))
        player_id = await cursor.fetchone()
        if player_id is None:
            embed = none_embed
            await interaction.followup.send(embed=embed, ephemeral= True)
        else:
            player_id = player_id[0]
            if type(player_id) != str: str(player_id)
            loading_embed = loadingEmbed(text = '區域道具')
            await interaction.followup.send(embed=loading_embed)
            embed_list = await get_user_area_items(player_id, self.bot.session)
            embed_list[0].set_author(name=person.display_name, icon_url= person.display_avatar)
            await GeneralPaginator(interaction, embed_list).start(embeded=True, follow_up=True)
    
    @app_commands.command(name='user-music', description='查看所有歌曲') 
    @app_commands.rename(person='其他玩家')
    async def user_music(self, interaction: discord.Interaction, person: discord.User=None): 
        group_select = Select(placeholder='選擇歌曲分類', options = [
        
        SelectOption(label='虛擬歌手', value ='vocaloid', 
                    description='バーチャル・シンガー', 
                    ), 
        
        SelectOption(label='25點，Nightcord見。', value ='school_refusal', 
                    description='25時、ナイトコードで。', 
                    emoji= group_icon_square['school_refusal']
                    ), 
        
        SelectOption(label='Leo/need', value ='light_music_club', 
                    description='Leo/need', 
                    emoji= group_icon_square['light_music_club']
                    ), 
        
        SelectOption(label='MORE MORE JUMP！', value ='idol', 
                    description='MORE MORE JUMP！', 
                    emoji= group_icon_square['idol']
                    ), 
        
        SelectOption(label='Vivid BAD SQUAD', value ='street', 
                    description='Vivid BAD SQUAD', 
                    emoji= group_icon_square['street']
                    ), 
        
        SelectOption(label='Wonderlands×Showtime', value ='theme_park', 
                    description='ワンダーランズ×ショウタイム', 
                    emoji= group_icon_square['theme_park']
                    ),
        
        SelectOption(label='其他', value ='other'), 
                                                                    ])   
        
        async def group_select_callback(interaction: discord.Interaction):  
            await interaction.response.defer()
            all_music = await get_group_music(session) 
            all_options = []
            
            for music in all_music[f'{group_select.values[0]}']:
                music_name = music[0]
                music_id = music[1]
                all_options.append(SelectOption(label=music_name, value=f'{music_id}'))
            
            class song_select(Select):
                async def callback(self, interaction: discord.Interaction):
                    await interaction.response.defer()
                    ayaakaa = await is_ayaakaa(interaction)
                    
                    if ayaakaa == True: 
                        db = await aiosqlite.connect("kanade_data.db")
                        cursor = await db.cursor()
                        
                        if person == None:
                            discord_id = interaction.user.id
                        else:
                            discord_id = person.id
                            
                        await cursor.execute('SELECT player_id from user_accounts WHERE discord_id = ?', (str(discord_id),))
                        player_id = await cursor.fetchone()
                        
                        if player_id is None:
                            embed = none_embed
                            await interaction.followup.send(embed=embed, ephemeral= True)
                        else:
                            player_id = player_id[0]
                            embed_list = await get_user_music(import_id=player_id, music_id=self.values[0], session=session)
                            await GeneralPaginator(interaction, embed_list).start(embeded=True, follow_up=True)
                            
            def divide_list(lst, n):
                #將一個 list 分為大小為 n 的等分
                for i in range(0, len(lst), n):
                    yield lst[i:i + n] 
                    
            divided_options = list(divide_list(lst=all_options, n=25))
            view = View()  
            for options in divided_options:
                view.add_item(song_select(placeholder="選擇歌曲", options=options))       
            await interaction.followup.send(view=view)
            
        group_select.callback = group_select_callback
        view = View()
        view.add_item(group_select)
        await interaction.response.send_message(view=view)
    '''
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SekaiProfileCog(bot))
