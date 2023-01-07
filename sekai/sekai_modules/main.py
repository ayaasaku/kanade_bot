import aiohttp

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
            
    elif type == 'diff':
        if server == 'tw':
            url = tw_diff
        elif server == 'jp':
            url = jp_diff
    
    data = f'{url}{path}'
    
    async with session.get(data) as r:
        return await r.json(content_type=f'{content_type}')