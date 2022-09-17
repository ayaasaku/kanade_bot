import time, discord, asyncio
from discord import app_commands, Interaction
from discord.ext import commands
from discord.app_commands import Choice

from utility.utils import defaultEmbed
from utility.apps.sekai.user.profile import user_profile
from utility.apps.sekai.user.data_processing import *

class ProfileCog(commands.Cog, name='profile'):
    def __init__(self, bot):
        self.bot = bot
        

        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ProfileCog(bot))