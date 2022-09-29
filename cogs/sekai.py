from types import NoneType
import aiosqlite

import discord
from discord import app_commands, ui
from discord.ext import commands
from discord.app_commands import Choice

from utility.utils import defaultEmbed, loadingEmbed, errEmbed, Convert
from utility.apps.sekai.user.profile import user_profile
from utility.apps.sekai.api_functions import get_sekai_user_api
from utility.apps.sekai.user.data_processing import *
from utility.apps.sekai.user.register import check_user_account

class SekaiCog(commands.Cog, name='sekai'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
        
    #await cursor.execute('CREATE TABLE user_accounts (discord_id INTEGER, player_id INTEGER)')    
    
    class RegisterModal(discord.ui.Modal, title=f'註冊帳戶'):           
        player_id = ui.TextInput(label='玩家id', style=discord.TextStyle.short, required=True)
        
        async def on_submit(self, interaction: discord.Interaction):
            db = await aiosqlite.connect("kanade_data.db")
            cursor = await db.cursor()
            discord_id = str(interaction.user.id)
            player_id = str(self.player_id)
            name = interaction.user.display_name
            await cursor.execute('INSERT INTO user_accounts(discord_id, player_id) VALUES(?, ?)', (discord_id, player_id))
            await db.commit()
            title = '** 成功 **'
            description = f'{name}，感謝使用奏寶，帳號已設置成功。'
            embed = defaultEmbed(title, description)
            embed.set_author(name=interaction.user.display_name, icon_url= interaction.user.display_avatar)
            embed.add_field(name=f'ID: ', value=self.player_id, inline=False)
            await interaction.response.send_message(embed=embed, ephemeral= True)

    @app_commands.command(name='register', description='register-player-id')    
    async def register(self, interaction: discord.Interaction):
        db = await aiosqlite.connect("kanade_data.db")
        check = await check_user_account(discord_id = interaction.user.id, db=db)
        if check == False:
            await interaction.response.send_modal(self.RegisterModal())
        else:
            embed = errEmbed(
            '帳號已經存在',
            f'你已經註冊過帳號了，不需要再註冊囉')
            await interaction.response.send_message(embed=embed)
          
    @app_commands.command(name='remove', description='remove-user-account')
    @app_commands.checks.has_role('小雪團隊')
    async def remove(self, interaction: discord.Interaction):
        discord_id = interaction.user.id
        db = await aiosqlite.connect("kanade_data.db")
        cursor = await db.cursor()
        await cursor.execute('SELECT player_id from user_accounts WHERE discord_id = ?', (str(interaction.user.id),))
        player_id = await cursor.fetchone()
        await cursor.execute('DELETE FROM user_accounts WHERE discord_id = ?', (str(discord_id),))
        await cursor.execute('DELETE FROM user_accounts WHERE player_id = ?', (str(player_id),))
        await db.commit()
        await interaction.response.send_message('成功')
        
    @app_commands.command(name='profile', description='查看一個玩家的帳戶') 
    @app_commands.rename(person='其他玩家')
    async def profile(self, interaction: discord.Interaction, person: discord.User = False):
        await interaction.response.defer()
        db = await aiosqlite.connect("kanade_data.db")
        cursor = await db.cursor()
        if person == False:
            discord_id = interaction.user.id
        else:
            discord_id = person.id
        await cursor.execute('SELECT player_id from user_accounts WHERE discord_id = ?', (str(discord_id),))
        player_id = await cursor.fetchone()
        player_id = player_id[0]
        loading_embed = loadingEmbed(text = '玩家', img = 'https://static.wikia.nocookie.net/projectsekai/images/b/bb/Yoisaki_Kanade_chibi.png/revision/latest?cb=20220320041840', thumbnail = True)
        await interaction.followup.send(embed=loading_embed, ephemeral=True)
        embed = await user_profile(player_id, self.bot.session)
        await interaction.followup.send(embed=embed)
        
async def setup(bot: commands.Bot) -> NoneType:
    await bot.add_cog(SekaiCog(bot))