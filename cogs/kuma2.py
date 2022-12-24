import discord
from discord import Member
from discord.ext import commands

from utility.utils import is_ayaakaa, defaultEmbed

class Kuma2Cog(commands.Cog, name='kuma2'):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        if member.guild.id == 1000043106164539453: #1001466950309924876:
            #await member.add_roles([1001478249773289562,], reason = 'New Member', atomic = True)
            await member.add_roles([1056048151125037098,], reason = 'New Member', atomic = True)
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Kuma2Cog(bot))