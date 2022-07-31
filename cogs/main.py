import random
from datetime import datetime
from random import randint

import discord
from data.user_data import morning, special
from discord import app_commands
from discord.ext import commands
from utility.utils import defaultEmbed
from data.version import version

class MainCog(commands.Cog, name='main'):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        user_id = message.author.id
        user = self.bot.get_user(message.author.id)
        morning_list = ['早安呀...', '早安喔...', '早安...',
                        '早安安...', '早安', '早', '早...', '早呀...', '早喔...']
        noon_list = ['午安呀...', '午安喔...', '午安安...', '午安', '午', '午安...', '午...']
        night_list = ['晚安呀...', '晚安喔...', '晚安安...', '晚安', '晚安...', '晚', '晚...']
        now = datetime.now()

        if message.author.bot:
            return

        if "早" in message.content or "午" in message.content or "晚" in message.content:
            if "奏" in message.content and "早" in message.content:
                start = datetime(year=now.year, month=now.month,
                                 day=now.day, hour=5, minute=0, second=0, microsecond=0)
                end = datetime(year=now.year, month=now.month, day=now.day,
                               hour=11, minute=59, second=0, microsecond=0)
                if start <= now <= end:
                    author = morning.get(
                        message.author.id) or message.author.display_name
                    await message.reply(f'{author}{random.choice(morning_list)}')
            elif "奏" in message.content and "午" in message.content:
                start = datetime(year=now.year, month=now.month, day=now.day,
                                 hour=12, minute=0, second=0, microsecond=0)
                end = datetime(year=now.year, month=now.month, day=now.day,
                               hour=17, minute=59, second=0, microsecond=0)
                if start <= now <= end:
                    author = morning.get(
                        message.author.id) or message.author.display_name
                    await message.reply(f'{author}{random.choice(noon_list)}')
            elif "奏" in message.content and "晚" in message.content:
                author = morning.get(
                    message.author.id) or message.author.display_name
                await message.reply(f'{author}{random.choice(night_list)}')

            '''elif "不" not in message.content and "奏" in message.content and "愛" in message.content or "奏" in message.content and "喜歡" in message.content:
            if message.author.id == special['ayaakaa']['user_id']:
                await message.reply(f'奏最喜歡霞霞了！🤍')
            elif message.author.id == special['seria']['user_id']:
                await message.reply(f'雪... 🤍')'''
                
        elif "我愛奏" in message.content or "我喜歡奏" in message.content:
                if message.author.id == 427346531260301312:
                    await message.reply(f'奏不喜歡怪叔叔... <:angry_fbk:981195991137013830>')
                else:    
                    await message.reply(f'奏也愛你...')
        
        elif "召喚" in message.content and "奏" in message.content:
                await message.reply(f'召喚成功...')

    @app_commands.command(name='about', description='有關奏寶')
    async def about(self, interaction: discord.Interaction):
        embed = defaultEmbed(title="奏寶 • Kanade Bot",
                             description="**奏寶**是由**綾霞**製作的機器人，並由小雪團隊協助開發")
        embed.set_author(name="奏寶", url="https://github.com/Ayaakaa/kanade_bot",
                         icon_url="https://i.imgur.com/oXEl8tP.jpg")
        embed.set_image(url="https://i.imgur.com/ZW5OWx8.png")
        embed.set_footer(text=f"奏寶 v{version} - by Ayaakaa@Seria Studios",
                     icon_url="https://imgur.com/HwcMqPS.png")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='say', description='用奏寶說話')
    @app_commands.checks.has_role('小雪團隊')
    async def say(self, i: discord.Interaction, message: str):
        await i.response.send_message('成功', ephemeral=True)
        await i.channel.send(message)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MainCog(bot))
