import logging
import discord
from discord import Colour, Interaction, User, Client 
from datetime import datetime



#ayaakaa
async def is_ayaakaa (self, i: Interaction):
    if i.user.id != 831883841417248778:
        await i.response.send_message(embed=self.notAyaakaaEmbed(), ephemeral=True)
        return False
    else:
        return True

#embeds    
def defaultEmbed(title: str = '', description: str = ''):
    embed = discord.Embed(title=title, description=description, color=0xBB6688)
    return embed

def loadingEmbed(text: str):
    embed = discord.Embed(title=f'**正在獲取{text}資料...**', description=f'獲取資料需時，請耐心等候', color=discord.Colour.from_str('0xBB6688'))
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1031194857747775680.gif?size=240&quality=lossless')
    return embed     

def errEmbed(title: str = '', message: str = ''):
    embed = discord.Embed(title=title, description=message, color=discord.Colour.from_str('#F13650'))
    return embed

def errMsgEmbed(title: str = '', message: str = ''):
    embed = discord.Embed(title=title, description=message, color=discord.Colour.from_str('#F13650'))
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1031194641816633364.gif?size=240&quality=lossless')
    embed.set_footer(text=f"如果你認為這是一個 BUG，歡迎私訊綾霞 ayaakaa#9815", 
                    icon_url="https://avatars.githubusercontent.com/u/80079457?v=4")
    return embed

def notAyaakaaEmbed():
    embed = discord.Embed(title=f'權限不足', description=f'你不是綾霞', color=discord.Colour.from_str('#F13650'))
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1031194641816633364.gif?size=240&quality=lossless')
    return embed

def successEmbed(title: str = '', message: str = ''):
    embed = discord.Embed(title=title, description=message, color=discord.Colour.from_str('#3DC05F'))
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1031194625819553882.webp?size=240&quality=lossless')
    return embed

#log
def log(is_system: bool, is_error: bool, log_type: str, log_msg: str):
    now = datetime.now()
    today = datetime.today()
    current_date = today.strftime('%Y-%m-%d')
    current_time = now.strftime("%H:%M:%S")
    system = "SYSTEM"
    if not is_system:
        system = "USER"
    if not is_error:
        log_str = f"<{current_date} {current_time}> [{system}] ({log_type}) {log_msg}"
    else:
        log_str = f"<{current_date} {current_time}> [{system}] [ERROR] ({log_type}) {log_msg}"
    with open('log.txt', 'a+', encoding='utf-8') as f:
        f.write(f'{log_str}\n')
    return log_str

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
 
