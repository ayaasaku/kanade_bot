import requests, json, aiohttp

#events
async def get_sekai_current_event_standings_api_jp(session: aiohttp.ClientSession, event_id):
        api = f'https://bitbucket.org/sekai-world/sekai-event-track/raw/f6f3fc4311a8cdd4bba5cedebcef02ff994939d5/event{event_id}.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

async def get_sekai_world_events_api_jp(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/master/events.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
async def get_sekai_current_event_api_jp(session: aiohttp.ClientSession):
        api = f'https://sekaidb.xyz/l10n/event/en.json'
        async with session.get(api) as r:
            return await r.json()

async def get_sekai_master_api_jp(session: aiohttp.ClientSession):
        api = f'https://sekaidb.xyz/db/prod.json'
        async with session.get(api) as r:
            return await r.json()

async def get_sekai_events_api_jp(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/master/events.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

async def get_sekai_event_deck_bonuses_api_jp(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/master/eventDeckBonuses.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
#events
async def get_sekai_current_event_standings_api_tw(event_id, session: aiohttp.ClientSession):
        api = f'https://bitbucket.org/sekai-world/sekai-event-track/raw/f6f3fc4311a8cdd4bba5cedebcef02ff994939d5/event{event_id}.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

async def get_sekai_world_events_api_tw(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/master/events.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
async def get_sekai_current_event_api_tw(session: aiohttp.ClientSession):
        api = f'https://sekaidb.xyz/l10n/event/en.json'
        async with session.get(api) as r:
            return await r.json()

async def get_sekai_master_api_tw(session: aiohttp.ClientSession):
        api = f'https://sekaidb.xyz/db/prod.json'
        async with session.get(api) as r:
            return await r.json()

async def get_sekai_events_api_tw(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/master/events.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

async def get_sekai_event_deck_bonuses_api_tw(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/master/eventDeckBonuses.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')

#songs
async def get_sekai_musics_api(session: aiohttp.ClientSession):
    api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musics.json'
    async with session.get(api) as r:
        return await r.json(content_type='text/plain')
        
async def get_sekai_music_difficulties_api(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musicDifficulties.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
async def get_sekai_music_vocals_api(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musicVocals.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
async def get_sekai_music_tags_api(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/main/musicTags.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
async def get_sekai_characters_info_api(session: aiohttp.ClientSession):
        api = f'https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/main/gameCharacters.json'
        async with session.get(api) as r:
            return await r.json(content_type='text/plain')
        
