import aiohttp
import time
from utility.apps.sekai.api_functions import (get_sekai_virtual_live_api_tw, get_sekai_virtual_live_api_jp)
from utility.apps.sekai.time_formatting import (format_date, format_date_jp)
from data.channel_list import channel_list
from utility.utils import defaultEmbed

async def get_current_virtual_live(server: str, session: aiohttp.ClientSession):
    if server == 'tw':
        api = await get_sekai_virtual_live_api_tw(session)
    elif server == 'jp':
        api = await get_sekai_virtual_live_api_jp(session)
    empty =[]
    live_list = []
    for live in api:
        virtual_live_start_time = live['startAt']
        virtual_live_end_time = live['endAt']
        current_time = int(time.time())
        current_time *= 1000
        if current_time >= virtual_live_start_time and current_time <= virtual_live_end_time:
            live_list.append(live)
    if live_list == empty or live_list == None:
        return None
    else:
        return live_list

async def get_current_virtual_live_embed(server: str, session: aiohttp.ClientSession):
    live_list = await get_current_virtual_live(server, session)
    if live_list == None:
        return None
    else:
        if len(live_list) == 1:
            name = live_list[0]['name']
            start_at = live_list[0]['startAt']
            if type(start_at) != int:
                start_at = int(start_at)
            start_at //= 1000
            end_at = live_list[0]['endAt']
            if type(end_at) != int:
                end_at = int(end_at)
            end_at //= 1000
            if server == 'tw':
                start_at = await format_date(start_at)
                end_at = await format_date(end_at)
                img = f'https://storage.sekai.best/sekai-tc-assets/virtual_live/select/banner/{asset_name}_rip/{asset_name}.webp'
            elif server == 'jp':
                start_at = await format_date_jp(start_at)
                end_at = await format_date_jp(end_at)
                img = f'https://storage.sekai.best/sekai-assets/virtual_live/select/banner/{asset_name}_rip/{asset_name}.webp'
            asset_name = live_list[0]['assetbundleName']
            embed = defaultEmbed(name)
            embed.set_image(url=img)
            embed.add_field(name='開始於', value = start_at, inline= False)
            embed.add_field(name='結束於', value = end_at, inline= False)
            return embed
        else:
            embed_list = []
            for live in live_list:
                name = live['name']
                start_at = live['startAt']
                if type(start_at) != int:
                    start_at = int(start_at)
                start_at //= 1000
                end_at = live['endAt']
                if type(end_at) != int:
                    end_at = int(end_at)
                end_at //= 1000
                asset_name = live['assetbundleName']
                if server == 'tw':
                    start_at = await format_date(start_at)
                    end_at = await format_date(end_at)
                    img = f'https://storage.sekai.best/sekai-tc-assets/virtual_live/select/banner/{asset_name}_rip/{asset_name}.webp'
                elif server == 'jp':
                    start_at = await format_date_jp(start_at)
                    end_at = await format_date_jp(end_at)
                    img = f'https://storage.sekai.best/sekai-assets/virtual_live/select/banner/{asset_name}_rip/{asset_name}.webp'
                embed = defaultEmbed(name)
                embed.set_image(url=img)
                embed.add_field(name='開始於', value = start_at, inline= False)
                embed.add_field(name='結束於', value = end_at, inline= False)
                embed_list.append(embed)
            return embed_list
            

async def virtual_live_ping_tw(bot, session: aiohttp.ClientSession):
    live_list = await get_current_virtual_live('tw', session)
    if live_list != None:
        for current_virtual_live in live_list:
            for thing in current_virtual_live['virtualLiveSchedules']:
                name = current_virtual_live['name']
                asset_name = current_virtual_live['assetbundleName']
                virtual_live_start_time = thing['startAt']
                virtual_live_start_time //= 1000
                current_time = int(time.time())
                if current_time == virtual_live_start_time - 300:
                    embed = defaultEmbed(title= f'虛擬 Live 即將開始', description=f'{name} 將於五分鐘後開始')
                    img = f'https://storage.sekai.best/sekai-tc-assets/virtual_live/select/banner/{asset_name}_rip/{asset_name}.webp'
                    embed.set_image(url=img)
                    for i in channel_list:           
                        channel = bot.get_channel(i)
                        await channel.send(embed=embed)

async def virtual_live_ping_jp(bot, session: aiohttp.ClientSession):
    live_list = await get_current_virtual_live('jp', session)
    if live_list != None:
        for current_virtual_live in live_list:
            for thing in current_virtual_live['virtualLiveSchedules']:
                name = current_virtual_live['name']
                asset_name = current_virtual_live['assetbundleName']
                virtual_live_start_time = thing['startAt']
                virtual_live_start_time //= 1000
                current_time = int(time.time())
                if current_time == virtual_live_start_time - 300:
                    embed = defaultEmbed(title= f'虛擬 Live 即將開始', description=f'{name} 將於五分鐘後開始')
                    img = f'https://storage.sekai.best/sekai-assets/virtual_live/select/banner/{asset_name}_rip/{asset_name}.webp'
                    embed.set_image(url=img)
                    for i in channel_list:           
                        channel = bot.get_channel(i)
                        await channel.send(embed=embed)