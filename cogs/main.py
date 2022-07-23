import calendar
import uuid
from datetime import datetime
from typing import Any, List

import aiosqlite
import discord
from dateutil import parser
from debug import DefaultView
from discord import Button, Interaction, Member, SelectOption, app_commands
from discord.app_commands import Choice
from discord.ext import commands
from discord.ui import Select
from utility.apps.FlowApp import FlowApp
from utility.utils import defaultEmbed, errEmbed, log
from data.user_data import morning

import random
from random import randint

class MorningCog(commands.Cog, name='flow'):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.debug_toggle = self.bot.debug_toggle   
    @commands.Cog.listener()
    async def on_message(self, message):
        user_id = message.author.id
        user = self.bot.get_user(message.author.id)
        if message.author.bot:
            return
        
        morning_list = ['早安呀', '早安喔', '早安哇', '早安安', '早安', '早', '早呀', '早喔', '早哇']
        noon_list = ['午安呀', '午安喔', '午安哇', '午安安', '午安', '午']
        night_list = ['晚安呀', '晚安喔', '晚安哇', '晚安安', '晚安', '晚']


        if "早" in message.content or "午" in message.content or "晚" in message.content:
            if "早" in message.content:
                start = datetime(year=now.year, month=now.month,
                                 day=now.day, hour=5, minute=0, second=0, microsecond=0)
                end = datetime(year=now.year, month=now.month, day=now.day,
                               hour=11, minute=59, second=0, microsecond=0)
                if start <= now <= end:
                    author = morning.get(message.author.id) or message.author.display_name
                    await message.reply(f'{author}{random.choice(morning_list)}')
            elif "午" in message.content:
                start = datetime(year=now.year, month=now.month, day=now.day,
                                 hour=12, minute=0, second=0, microsecond=0)
                end = datetime(year=now.year, month=now.month, day=now.day,
                               hour=17, minute=59, second=0, microsecond=0)
                if start <= now <= end:
                    author = morning.get(message.author.id) or message.author.display_name
                    await message.reply(f'{author}{random.choice(noon_list)}')
            elif "晚" in message.content:
                    author = morning.get(message.author.id) or message.author.display_name
                    await message.reply(f'{author}{random.choice(morning_list)}')
                        
class AboutCog(commands.Cog, name='about'):
    def __init__(self, bot):
        self.bot = bot   
    @app_commands.command(name='about', description='有關奏寶 - About Kanade')
    async def snow(self, interaction: discord.Interaction):
        await interaction.response.send_message("")