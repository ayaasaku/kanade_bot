import aiohttp
from datetime import (datetime, timedelta)

from sekai.sekai_modules.data import (api, jp_asset, tw_asset, jp_diff, tw_diff)

async def get_data(server: str, type: str, path: str ,session: aiohttp.ClientSession):
    #raise error
    possible_server = ['tw','jp']
    possible_type = ['api', 'diff', 'assets']
    if server not in possible_server:
        raise ValueError(f'Server {server} is not supported, it must be tw or jp')
    if type not in possible_type:
        raise ValueError(f'Type {type} is not supported, it must be api or diff or assets')
    
    #run
    content_type = 'text/plain'
    
    if type == 'api':
        url = api
        content_type = 'text/html'
        
    elif type == 'assets':
        if server == 'tw':
            url = tw_asset
        elif server == 'jp':
            url = jp_asset
        data = f'{url}{path}'
        return data
            
    elif type == 'diff':
        if server == 'tw':
            url = tw_diff
        elif server == 'jp':
            url = jp_diff
    
    data = f'{url}{path}'
    
    async with session.get(data) as r:
        json = await r.json(content_type=f'{content_type}')
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