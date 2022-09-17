import time, discord, asyncio
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from utility.utils import defaultEmbed
from utility.apps.sekai.user.profile import user_profile
from utility.apps.sekai.user.data_processing import *

class ProfileCog(commands.Cog, name='profile'):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='profile', description='查看一個玩家的帳戶')    
    async def profile(self, interaction: discord.Interaction):
        interaction.response.defer()
        user_id = 244775114281091084
        embed = await user_profile(user_id, self.bot.session)
        interaction.followup.send(embed=embed)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ProfileCog(bot))