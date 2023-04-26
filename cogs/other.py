from discord import Member
from discord.ext import commands


class OtherCog(commands.Cog, name='other'):
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        if member.guild.id == 1001466950309924876:
            role = member.guild.get_role(1001478249773289562)
            await member.add_roles(role)
            
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OtherCog(bot))