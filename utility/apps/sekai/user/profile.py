import aiohttp

import discord
from discord import Embed, app_commands, embeds
from discord.app_commands import Choice
from discord.ext import commands
from numpy import append

from utility.apps.sekai.time_formatting import format_date_jp
from utility.apps.sekai.user.data_processing import (get_profile_img,
                                                     get_user_decks,
                                                     get_user_game_data,
                                                     get_user_profile,
                                                     get_user_profile_pic,
                                                     get_user_character_level)
from utility.utils import defaultEmbed
from data.emoji_data import charater_icons

async def user_profile(import_id: str, session: aiohttp.ClientSession):
    get_id = await get_user_game_data(import_id, 'userId', session)
    if import_id == str(get_id):
        name = await get_user_game_data(import_id, 'name', session)
        rank = await get_user_game_data(import_id, 'rank', session)
        word = await get_user_profile(import_id, 'word', session)
        leader_id = await get_user_decks(import_id, 'leader', session)
        tl_url = await get_user_profile_pic(import_id, leader_id, session)  
        img_url = await get_profile_img(leader_id, session)  
        if word == None or len(word) < 1: word = '此玩家並沒有設置簡介'
        seconds = int((1600218000000 + int(import_id) / 2 ** 22) + 25200000)
        creation_date = await format_date_jp (seconds)
        characters_level_list = await get_user_character_level(import_id, session)
        
        embed = defaultEmbed(title=f'**{name}**', description=f'「{word}」')
        embed.set_thumbnail(url=tl_url)
        if img_url != None:
            embed.set_image(url=img_url)
        embed.add_field(name=f'等級：', value=rank, inline=False)
        embed.add_field(name=f'創建日期：', value=f'{creation_date}', inline=False)
        
        embed2 = defaultEmbed(title=f'**角色等級**')
        embed2.set_footer(text=f'玩家ID：{import_id}', icon_url=f'{tl_url}')
        for character in characters_level_list:
            character_list_emoji = []
            character_list_level = []
            id = character['characterId']
            level = character['characterRank']
            emoji = charater_icons[f'chr_ts_90_{id}']
            character_list_emoji.append(emoji)
            character_list_level.append(str(level))
        description = (
            emoji[0]+level[0]+'\u200b'+emoji[1]+level[1]+'\u200b'+emoji[2]+level[2]+'\n'\
            +emoji[3]+level[3]+'\u200b'+emoji[4]+level[4]+'\u200b'+emoji[5]+level[5]+'\n'\
            +emoji[6]+level[6]+'\u200b'+emoji[7]+level[7]+'\u200b'+emoji[8]+level[8]+'\n'\
            +emoji[9]+level[9]+'\u200b'+emoji[10]+level[10]+'\u200b'+emoji[11]+level[11]+'\n'\
            +emoji[12]+level[12]+'\u200b'+emoji[13]+level[13]+'\u200b'+emoji[14]+level[14]+'\n'\
            +emoji[15]+level[15]+'\u200b'+emoji[16]+level[16]+'\u200b'+emoji[17]+level[17]+'\n'\
            +emoji[18]+level[18]+'\u200b'+emoji[19]+level[19]+'\u200b'+emoji[20]+level[20]+'\n'\
            +emoji[21]+level[21]+'\u200b'+emoji[22]+level[22]+'\u200b'+emoji[23]+level[23]+'\n'\
            +emoji[24]+level[24]+'\u200b'+emoji[25]+level[25]+'\u200b'+emoji[26]+level[26])

        embed2.description = description
        embed_list = [embed, embed2]
        return embed_list
