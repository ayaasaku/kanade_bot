import time, discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from utility.utils import defaultEmbed
from utility.apps.sekai.user.profile import user_profile

class ProfileCog(commands.Cog, name='profile'):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='profile', description='查看一個玩家的帳戶')    
    #@app_commands.rename(user_id='玩家id')           
    async def profile(self, interaction: discord.Interaction):#, user_id: int): 
        interaction.response.defer
        user_id = 244775114281091084 
        message = await user_profile(user_id, self.bot.session)
        await interaction.followup.send(str(message))
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ProfileCog(bot))