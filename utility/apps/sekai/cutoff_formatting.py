from datetime import datetime,timedelta
from pytz import timezone
from tabulate import tabulate
import re, time, discord
import requests, json, aiohttp

from utility.utils import defaultEmbed

from utility.apps.sekai.event_info import get_current_event_id_jp,get_event_end_time_jp, get_event_banner_name_jp, get_event_name_jp
from utility.apps.sekai.api_functions import get_sekai_world_events_api_jp, get_sekai_current_event_standings_api_jp, get_sekai_current_event_api_jp
from utility.apps.sekai.time_formatting import format_time

async def get_cutoff_formatting(session: aiohttp.ClientSession, tier: str = '0'):
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    now_time = datetime.now(timezone('Asia/Taipei'))
    entries = []
    event_id = await get_current_event_id_jp(session)
    #event_id = 10
    event_name = await get_event_name_jp(event_id, session)
    current_event_cutoff_api = await get_sekai_current_event_standings_api_jp(event_id, session)
    last_updated_time = time.time() - (current_event_cutoff_api['time'] / 1000)
    last_updated_time = f"{await format_time(last_updated_time)} ago"
    #print(f"Current time: {time.time() * 1000}\nAPI Time: {current_event_cutoff_api['time']}")
    
    if tier == '0': # all cutoffs
        for x in current_event_cutoff_api: 
            if x != 'time':
                for y in current_event_cutoff_api[x]:
                    name = string_check(y['name'])
                    entries.append([
                        "{:,}".format(y['rank']),
                        "{:,}".format(y['score']),
                        y['userId'],
                        str(name)   
                    ])   
        #output = ("```" + f"  Event: {event_name}\n  Time: {now_time.strftime(fmt)}\n  \Last Updated: {last_updated_time}" + "\n\n" + tabulate(entries, tablefmt="plain", headers=["#", "Points", "ID", "Player"]) + "```")
        output = f'``` Event: {event_name}\n Time: {now_time.strftime(fmt)}\n \Last Updated: {last_updated_time}\n\n  {tabulate(entries, tablefmt="plain", headers=["#", "Points", "ID", "Player"])}```'
        return output
    
    elif tier == '10':
        for x in current_event_cutoff_api['first10']:
            name = string_check(x['name'])
            entries.append([
                "{:,}".format(x['rank']),
                "{:,}".format(x['score']),
                x['userId'],
                str(name)   
            ])
        #output = ("```" + f"  Event: {event_name}\n  Time: {now_time.strftime(fmt)}\n  Last Updated: {last_updated_time}" + "\n\n" + tabulate(entries, tablefmt="plain", headers=["#", "Points", "ID", "Player"]) + "```")
        output = f'``` Event: {event_name}\n Time: {now_time.strftime(fmt)}\n \Last Updated: {last_updated_time}\n\n  {tabulate(entries, tablefmt="plain", headers=["#", "Points", "ID", "Player"])}```'
        return output
    
    elif f'rank{tier}' in current_event_cutoff_api:
        
        event_banner_name = await get_event_banner_name_jp(event_id, session)
        logo_url = f"https://minio.dnaroma.eu/sekai-assets/event/{event_banner_name}/logo_rip/logo.webp"
        banner_url = f"https://minio.dnaroma.eu/sekai-assets/home/banner/{event_banner_name}_rip/{event_banner_name}.webp"
        event_id = await get_current_event_id_jp(session)
        event_end_time = (await get_event_end_time_jp(event_id, session)) / 1000
        current_time = time.time()
        if current_time > event_end_time:
            time_left = 'Event has ended'
        else:
            time_left = await format_time(event_end_time - current_time)
        event_url = f'https://sekai.best/event/{event_id}'
        embed=defaultEmbed(title=f"{event_name} [t{tier}]")
        embed.set_thumbnail(url=logo_url)
        embed.set_image(url=banner_url)
        embed.add_field(name='Current', value="{:,}".format(current_event_cutoff_api[f'rank{tier}'][0]['score']), inline=True)
        embed.add_field(name='Player', value=current_event_cutoff_api[f'rank{tier}'][0]['name'], inline=True)
        embed.add_field(name='ID', value=current_event_cutoff_api[f'rank{tier}'][0]['userId'], inline=True)
        embed.add_field(name='Last Updated', value=last_updated_time, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='Time Left', value=time_left, inline=True)
        embed.add_field(name='更多資訊', value=event_url, inline=False)
        embed.set_footer(text=f"{now_time.strftime(fmt)}")
        return embed

def string_check(string: str):
    import re
    string = string.replace('```','')
    string = string.replace("?",'')
    string = re.sub('(\[(\w{6}|\w{2})\])','', string)
    string = re.sub('\[([CcIiBbSsUu]|(sup|sub){1})\]', '', string) 
    return string
