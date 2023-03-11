import discord
from discord import app_commands, Interaction
from discord.ext import commands

from modules.main import defaultEmbed


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
    
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        tuple1 = ('奏寶：','奏奏：')
        tuple2 = ('奏寶:','奏奏:')
        if msg.author.id == 831883841417248778:
            global text
            if msg.content[0:3] in tuple1: text = msg.content.split('：')[1]
            elif msg.content[0:3] in tuple2: text = msg.content.split(': ')[1]
            if msg.type == 'reply':
                reply_id = msg.reference.message_id
                msg.delete()
                reply_message = discord.utils.get(await msg.channel.history(limit=100).flatten(), id=reply_id)
                await reply_message.reply(text)
            else:
                msg.delete()
                await msg.channel.send(text)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MainCog(bot))