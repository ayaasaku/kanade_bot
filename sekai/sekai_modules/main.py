import aiohttp
import os

from dotenv import load_dotenv
from datetime import (datetime, timedelta)

from data.emoji_data import common_materials
from sekai.sekai_modules.data import (api, jp_asset, tw_asset, jp_diff, tw_diff)


load_dotenv()
appid = os.getenv('APPID')
appsecret = os.getenv('APPSECRET')

async def get_data(server: str, type: str, path: str):
    #raise error
    possible_server = ['tw','jp']
    possible_type = ['api', 'diff', 'assets']
    if server not in possible_server:
        raise ValueError(f'Server {server} is not supported, it must be tw or jp')
    if type not in possible_type:
        raise ValueError(f'Type {type} is not supported, it must be api or diff or assets')
    
    #run
    content_type = 'text/plain'
    session = aiohttp.ClientSession()
    
    if type == 'api':
        url = api
        content_type = 'application/json'
        headers = {'appid': f'{appid}', 'appsecret': f'{appsecret}'}
        session = aiohttp.ClientSession(headers=headers)
        
    elif type == 'assets':
        if server == 'tw':
            url = tw_asset
        elif server == 'jp':
            url = jp_asset
        link = f'{url}{path}'
        await session.close()
        return link
            
    elif type == 'diff':
        if server == 'tw':
            url = tw_diff
        elif server == 'jp':
            url = jp_diff
    
    data = f'{url}{path}'
    
    async with session.get(data) as r:
        json = await r.json(content_type=f'{content_type}')
        await session.close()
        return json    
    
    
#time formatting    
# Format time in Dd Hh Mm Ss format
def format_time(seconds: int):
    days = (seconds // 86400)
    hours = (seconds // 3600) % 24
    minutes = (seconds // 60) % 60
    seconds = seconds % 60
    output = f"{days}d {hours}h {minutes}m {seconds}s"
    return output

# Format seconds to approximate hours
def format_hour(seconds: int):
    hours = (seconds // 3600) 
    return hours

# Format date in YYYY-MM-DD HH:MM:SS UTC format
def format_date(server:str, seconds: int):
    possible_server = ['tw','jp']
    if server not in possible_server:
        raise ValueError(f'Server {server} is not supported, it must be tw or jp')
    date = datetime.fromtimestamp(seconds)
    if server == 'tw':
        date = date-timedelta(hours=0)
    elif server == 'jp':
        date = date-timedelta(hours=-1)
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    return date

def format_creation_date(seconds: int):
    datetime.fromtimestamp(seconds)
    date = date-timedelta(hours=-1)
    date = date.strftime("%A, %B %d, %Y %I:%M:%S")
    return date
    
def format_progress(end_time, start_time, current_time):
    event_length = end_time - start_time
    time_left = end_time - current_time
    event_prog = round((((event_length - time_left) / event_length) * 100), 2)
    return f"{event_prog}%"

async def process_resource_box_details(server, details: list):
    common = ('jewel', 'paid_jewel', 'coin', 'virtual_coin', 'live_point')
    non_common = ('material', 'honor', 'bonds_honor', 'bonds_honor_word', 'avatar_costume', 'costume_3d', 'gacha_ticket', 'skill_practice_ticket', 'practice_ticket', 'card', 'area_item', 'music', 'music_vocal', 'boost_item')
    path_dict = {
        'material': 'main/materials.json',
        'honor': 'main/honors.json', 
        'bonds_honor': 'main/bondsHonors.json', 
        'bonds_honor_word': 'main/bondsHonorWords.json', 
        'avatar_costume': 'main/avatarCostumes.json', 
        'costume_3d': 'main/costume3ds.json', 
        'gacha_ticket': 'main/gachaTickets.json', 
        'skill_practice_ticket': 'main/skillPracticeTickets.json', 
        'practice_ticket': 'main/practiceTickets.json', 
        'card': 'main/cards.json', 
        'area_item': 'main/areaItems.json', 
        'music': 'main/music.json', 
        'music_vocal': 'main/musicVocal.json', 
        'boost_item': 'main/boostItems.json', 
        }
    details_list = []
    for item in details:
        if item in common:
            resource_type = item['resourceType']
            resource_quantity = item['resourceQuantity']
            dict = {
                        'type': 'common',
                        'name': None,
                        'resource_type': resource_type,
                        'assetbundleName': None,
                        'quantity': resource_quantity,
                        'resource_level': None
                    }
        elif item in non_common:
            resource_type = item['resourceType']
            resource_id = item['resourceId']
            resource_quantity = item['resourceQuantity']
            try: resource_level = item['resourceLevel']
            except: resource_level = None
            path = path_dict[resource_type]
            data = get_data(server=f'{server}', type='diff', path=path)
            for item in data:
                if item['id'] == resource_id:
                    try: name = item['name']
                    except: name = None
                    try: assetbundleName = item['assetbundleName']
                    except: assetbundleName = None
                    dict = {
                        'type': 'non_common',
                        'name': name,
                        'assetbundleName': assetbundleName,
                        'quantity': resource_quantity,
                        'resource_level': resource_level
                    }
        details_list.append(dict)
    return details_list

async def get_resource_box(server: str, resource_box_purpose: str, id: int):
    data = await get_data(server=f'{server}', type='diff', path='main/resourceBoxes.json')  
    for box in data:
        if box['resourceBoxPurpose'] == resource_box_purpose and box['id'] == id :
            details_list = await process_resource_box_details(server=server, details=item['details'])
            string = ''
            for item in details_list:
                if item['type'] == 'common':
                    emoji = common_materials[item['resource_type']]
                    quantity = item['quantity']
                    text = f'{emoji}x{quantity} | '
                elif item['type'] == 'non_common':
                    name = item['name']
                    quantity = item['quantity']
                    level = item['resource_level']
                    if level != None or level is not None:
                        text = f'{name}x{quantity} lv.{level} | '
                    else:
                        text = f'{name}x{quantity} | '
                string += text
            if string[-3:] == ' | ':
                string = string[:-3]
            return string
                    