import discord
from discord.ext import commands
from discord import app_commands
import re
import requests
from dotenv import load_dotenv
import os
from PIL import Image, ImageColor
from io import BytesIO

from utility.utils import defaultEmbed

class ColorCog(commands.Cog, name='color'):
    
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != bot.user:
            hexRegexs = re.findall("#[A-Fa-f0-9]{6}", message.content)
            if hexRegexs:
                files = []
                for hexCode in hexRegexs:
                    img = Image.new("RGB", (32, 32), ImageColor.getrgb(hexCode))
                    with BytesIO() as image_binary:
                        img.save(image_binary, 'PNG')
                        image_binary.seek(0)
                        files.append(discord.File(fp=image_binary, filename=f'{hexCode[1:]}.png'))
            
                await message.channel.send(files=files)

            await bot.process_commands(message)

    @app_commands.command(name='color', description='color')
    @app_commands.rename(search='Hex-Code')
    async def color(self, ctx, search: str):
        files = []
        for hexCode in search:
            img = Image.new("RGB", (32, 32), ImageColor.getrgb(hexCode))
            with BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                files.append(discord.File(fp=image_binary, filename=f'{hexCode[1:]}.png'))
            
        await ctx.message.channel.send(files=files)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ColorCog(bot))