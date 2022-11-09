import aiohttp

#events   
async def get_sekai_events_api_jp(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/master/events.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

async def get_sekai_event_deck_bonuses_api_jp(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/master/eventDeckBonuses.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

async def get_sekai_events_api_tw(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/master/events.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

async def get_sekai_event_deck_bonuses_api_tw(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/master/eventDeckBonuses.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

#music        
async def get_sekai_musics_api(session: aiohttp.ClientSession):
    api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musics.json'
    async with session.get(api) as r:
        return await r.json(content_type='text/plain')
        
async def get_sekai_music_difficulties_api(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musicDifficulties.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
async def get_sekai_music_vocals_api(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musicVocals.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
async def get_sekai_music_tags_api(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musicTags.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
    
#other         
async def get_sekai_characters_info_api(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/main/gameCharacters.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
async def get_sekai_cards_info_api(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/cards.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
async def get_sekai_area_items_info_api(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/main/areaItems.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

async def get_sekai_area_items_level_info_api(session: aiohttp.ClientSession):
        api = 'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/main/areaItemLevels.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
  
async def get_sekai_virtual_live_api(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/main/virtualLives.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
              
async def get_sekai_user_api(user_id, session: aiohttp.ClientSession):
        api = f'https://api.pjsekai.moe/api/user/{user_id}/profile'
        async with session.get(api) as r:
            return await r.json(content_type='text/html')
        

        