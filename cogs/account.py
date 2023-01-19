import aiosqlite

import discord
from discord import Embed, app_commands, ui, SelectOption
from discord.ui import View, Select
from discord.ext import commands
from discord.app_commands import Choice
from matplotlib.pyplot import get

from modules.main import defaultEmbed, loadingEmbed, errEmbed, successEmbed, is_ayaakaa,notAyaakaaEmbed
from modules.paginator import GeneralPaginator
from account.modules.register import check_user_account
from sekai.sekai_modules.main import get_data

from data.emoji_data import *

class AccountCog(commands.Cog, name='account'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        global none_embed
        none_embed = errEmbed(
            '玩家ID不存在',
            f'也許該名玩家還沒注冊？\n可以使用 `/register` 來註冊') 
            
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
        def __init__(self):
            pass
        player_id = ui.TextInput(label='玩家id', style=discord.TextStyle.short, required=True)
        
        async def on_submit(self, interaction: discord.Interaction):
            db = await aiosqlite.connect("kanade_data.db")
            cursor = await db.cursor()
            discord_id = str(interaction.user.id)
            player_id = str(self.player_id)
            name = interaction.user.display_name
            api = await get_data(server='jp', type='api', path=f'user/{self.player_id}/profile')
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
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AccountCog(bot))