import discord
from discord import app_commands, Interaction, utils, channel
from discord.ext import commands


from utility.utils import defaultEmbed, is_ayaakaa, notAyaakaaEmbed


class MainCog(commands.Cog, name='main'):
    
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='about', description='有關奏寶')
    async def about(self, interaction: Interaction):
        embed = defaultEmbed(title="奏寶 • Kanade Bot",
                             description="**奏寶**是由**綾霞**製作的機器人")
        embed.set_author(name="奏寶", url="https://github.com/Ayaakaa/kanade_bot",
                         icon_url="https://i.imgur.com/oXEl8tP.jpg")
        embed.set_image(url="https://i.imgur.com/ZW5OWx8.png")
        embed.set_footer(text=f"奏寶 v{self.bot.version} - by 綾霞 Ayaakaa")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='say', description='用奏寶說話')
    async def say(self, i: Interaction, message: str):
        is_ayaakaa_ = await is_ayaakaa(i)
        if is_ayaakaa_ == True:
            await i.response.send_message('成功', ephemeral=True)
            await i.channel.send(message)


    @app_commands.command(name='leave-guild', description='leave-a-guild')
    async def guilds(self, i: Interaction, guild_name: str='', guild_id: int=0):
        is_ayaakaa_ = await is_ayaakaa(i)
        if is_ayaakaa_ == True:
            if len(guild_name) >= 1:
                guild = utils.get(self.bot.guilds, name=guild_name)
            elif guild_id != 0:
                guild = utils.get(self.bot.guilds, id=guild_id)
            else:
                await i.response.send_message("Error")
                return
            if guild is None:
                await i.response.send_message("I don't recognize that guild.")
                return
            await guild.leave()
            await i.response.send_message(f"Left guild: {guild.name} ({guild.id})")
    
    @app_commands.command(name='test', description='test')
    async def test(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(1020235653700665347)
        channel.send(f'test')
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MainCog(bot))
