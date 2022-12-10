import aiosqlite
import asyncio

import discord
from discord import Embed, app_commands, ui, SelectOption
from discord.ui import View, Select
from discord.ext import commands
from discord.app_commands import Choice
from matplotlib.pyplot import get

from utility.utils import defaultEmbed, loadingEmbed, errEmbed, successEmbed, is_ayaakaa,notAyaakaaEmbed
from utility.paginator import GeneralPaginator
from utility.apps.sekai.user.profile import user_profile
from utility.apps.sekai.user.data_processing import get_user_area_items, get_group_music
from utility.apps.sekai.api_functions import get_sekai_user_api, get_sekai_musics_api
from utility.apps.sekai.user.data_processing import *
from utility.apps.sekai.user.register import check_user_account

from data.emoji_data import *

class SekaiCog(commands.Cog, name='sekai'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        global session
        session = self.bot.session
        
        global none_embed
        none_embed = errEmbed(
            '玩家ID不存在',
            f'也許該名玩家還沒注冊？\n可以使用 `/register` 來註冊') 
    
    @app_commands.command(name='profile', description='查看一個玩家的帳戶') 
    @app_commands.rename(person='其他玩家')
    async def profile(self, interaction: discord.Interaction, person: discord.User = None):
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
            loading_embed = loadingEmbed(text = '玩家')
            await interaction.followup.send(embed=loading_embed)
            embed_list = await user_profile(player_id, self.bot.session)
            embed_list[0].set_author(name=person.display_name, icon_url= person.display_avatar)
            await GeneralPaginator(interaction, embed_list).start(embeded=True, follow_up=True)
            
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
        
    @app_commands.command(name='id', description='查看一個玩家的ID') 
    @app_commands.rename(person='其他玩家')
    async def id(self, interaction: discord.Interaction, person: discord.User = None):
        await interaction.response.defer()
        db = await aiosqlite.connect("kanade_data.db")
        cursor = await db.cursor()
        if person == None:
            discord_id = interaction.user.id
            name = interaction.user.display_name
            avatar = interaction.user.display_avatar
        else:
            discord_id = person.id
            name = person.display_name
            avatar = person.display_avatar
        await cursor.execute('SELECT player_id from user_accounts WHERE discord_id = ?', (str(discord_id),))
        player_id = await cursor.fetchone()
        if player_id is None:
            embed = none_embed
            await interaction.followup.send(embed=embed, ephemeral= True)
        else:
            player_id = player_id[0]
            embed = defaultEmbed(f'{player_id}')
            embed.set_author(name=f'{name}的玩家ID', icon_url=avatar)
            await interaction.followup.send(embed=embed)
        
    class RegisterModal(discord.ui.Modal, title=f'註冊帳戶'):           
        player_id = ui.TextInput(label='玩家id', style=discord.TextStyle.short, required=True)
        
        async def on_submit(self, interaction: discord.Interaction):
            db = await aiosqlite.connect("kanade_data.db")
            cursor = await db.cursor()
            discord_id = str(interaction.user.id)
            player_id = str(self.player_id)
            name = interaction.user.display_name
            api = await get_sekai_user_api(self.player_id, session)
            none = {}
            if api != none :  
                await cursor.execute('INSERT INTO user_accounts(discord_id, player_id) VALUES(?, ?)', (discord_id, player_id))
                await db.commit()
                title = '** 成功 **'
                description = f'{name}，感謝使用奏寶，帳號已設置成功。'
                embed = successEmbed(title, description)
                embed.set_author(name=interaction.user.display_name, icon_url= interaction.user.display_avatar)
                embed.add_field(name=f'ID: ', value=self.player_id, inline=False)
                await interaction.response.send_message(embed=embed, ephemeral= True)
            if api == none:
                embed = errEmbed(
                '玩家ID不存在',
                f'抱歉，目前只支持日服註冊\n請確定一下是否輸入了正確的ID')
                await interaction.response.send_message(embed=embed, ephemeral= True)

    @app_commands.command(name='register', description='註冊玩家ID')    
    async def register(self, interaction: discord.Interaction):
        db = await aiosqlite.connect("kanade_data.db")
        check = await check_user_account(discord_id = str(interaction.user.id), db=db)
        if check == False:
            await interaction.response.send_modal(self.RegisterModal())
        else:
            embed = errEmbed(
            '帳號已經存在',
            '你已經註冊過帳號了，不需要再註冊囉')
            await interaction.response.send_message(embed=embed)
          
    @app_commands.command(name='remove', description='remove-user-account')
    async def remove(self, interaction: discord.Interaction):
        is_ayaakaa_ = await is_ayaakaa(interaction)
        if is_ayaakaa_ == True:
            discord_id = interaction.user.id
            db = await aiosqlite.connect("kanade_data.db")
            cursor = await db.cursor()
            await cursor.execute('SELECT player_id from user_accounts WHERE discord_id = ?', (str(interaction.user.id),))
            player_id = await cursor.fetchone()
            await cursor.execute('DELETE FROM user_accounts WHERE discord_id = ?', (str(discord_id),))
            await cursor.execute('DELETE FROM user_accounts WHERE player_id = ?', (str(player_id),))
            await db.commit()
            await interaction.response.send_message('成功')
    
    @app_commands.command(name='user-music', description='查看所有歌曲') 
    @app_commands.rename(person='其他玩家')
    async def user_music(self, interaction: discord.Interaction, person: discord.User=None): 
        '''
        vocaloid_len = len(all_music['vocaloid'])
        light_music_club_len = len(all_music['light_music_club'])
        school_refusal_len = len(all_music['school_refusal'])
        idol_len = len(all_music['idol'])
        street_len = len(all_music['street'])
        theme_park_len = len(all_music['theme_park'])
        other_len = len(all_music['other'])
        
        print(f'vocaloid: {vocaloid_len}')
        print(f'light_music_club: {light_music_club_len}')
        print(f'school_refusal: {school_refusal_len}')
        print(f'idol: {idol_len}')
        print(f'street: {street_len}')
        print(f'theme_park: {theme_park_len}')
        print(f'other: {other_len}')
        '''
        
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
                    is_ayaakaa_ = await is_ayaakaa(interaction)
                    
                    if is_ayaakaa_ == True: 
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
                    
            divided_options = list(divide_list(lst=all_options, n=24))
            #print(divided_options)
            for options in divided_options:
                #print(f'{options}, len: {len(options)}')
                view = View()    
                view.add_item(song_select(placeholder="選擇歌曲", options=options))       
            await interaction.followup.send(view=view)
            
        group_select.callback = group_select_callback
        view = View()
        view.add_item(group_select)
        await interaction.response.send_message(view=view)
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SekaiCog(bot))
