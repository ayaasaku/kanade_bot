import aiosqlite, discord
from discord import app_commands, ui
from discord.ext import commands
from discord.app_commands import Choice

from utility.utils import loadingEmbed
from utility.apps.sekai.user.profile import user_profile
from utility.apps.sekai.user.data_processing import *

class SekaiCog(commands.Cog, name='sekai'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def setup(self):
        db = self.bot.db
        cursor = await db.cursor()
        await cursor.execute('CREATE TABLE user_accounts (discord_id INTEGER, player_id INTIGER)')
        await cursor.close()
        await db.commit()
        
    class Register(ui.Modal, title=f'註冊帳戶\n\u200b\n注意！目前只支持日服帳號的註冊'):
        player_id = ui.TextInput(label='玩家id', style=discord.TextStyle.short, required=True)
        
        async def on_submit(self, interaction: discord.Interaction):
            db = self.db
            cursor = self.cursor
            discord_id = interaction.user.id
            player_id = self.player_id
            await cursor.execute('INSERT INTO user_accounts (discord_id, player_id) VALUES (?, ?)', (discord_id, player_id))
            await db.commit()
            await interaction.response.send_message(f'{interaction.user.display_name}，感謝使用奏寶，帳號已設置成功', ephemeral= True)
            
            
        @app_commands.command(name='register', description='register-player-id')    
        async def register(self, interaction: discord.Interaction):
            await interaction.response.send_modal(self.Register)
        
    @app_commands.command(name='profile', description='查看一個玩家的帳戶')    
    async def profile(self, interaction: discord.Interaction):
        await interaction.response.defer()
        db = self.bot.db
        cursor = await db.cursor()
        await cursor.execute('SELECT player_id from user_accounts WHERE discord_id = ?', (interaction.user.id,))
        player_id = await cursor.fetchone()
        embed = loadingEmbed(text = '玩家', img = 'https://static.wikia.nocookie.net/projectsekai/images/b/bb/Yoisaki_Kanade_chibi.png/revision/latest?cb=20220320041840', thumbnail = True)
        await interaction.followup.send(embed=embed, ephemeral=True)
        embed = await user_profile(player_id, self.bot.session)
        await interaction.followup.send(embed=embed)

        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SekaiCog(bot))