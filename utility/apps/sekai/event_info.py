import re, aiohttp
from utility.apps.sekai.api_functions import get_sekai_world_events_api_jp, get_sekai_events_api_jp, get_sekai_event_deck_bonuses_api_jp, \
    get_sekai_world_events_api_tw, get_sekai_events_api_tw, get_sekai_event_deck_bonuses_api_tw, get_sekai_characters_info_api
#jp
async def get_current_event_id_jp(session: aiohttp.ClientSession):
    event_api = await get_sekai_world_events_api_jp(session)
    return event_api[-1]['id']

async def get_event_name_jp(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_events_api_jp(session)
    event_name = event_api[-1]['name']
    return event_name

async def get_event_type_jp(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_events_api_jp(session)
    event_name = event_api[-1]['eventType'].capitalize()
    return event_name

async def get_event_start_time_jp(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_events_api_jp(session)
    event_start_time = event_api[-1]['startAt']
    return event_start_time

async def get_event_end_time_jp(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_events_api_jp(session)
    event_end_time = event_api[-1]['aggregateAt']
    return event_end_time

async def get_event_banner_name_jp(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_events_api_jp(session)
    event_banner_name = event_api[-1]['assetbundleName']
    return event_banner_name

async def get_event_bonus_attribute_jp(session: aiohttp.ClientSession):
    event_api = await get_sekai_event_deck_bonuses_api_jp(session)
    event_bonus_attribute = event_api[-1]['cardAttr'].capitalize()
    return event_bonus_attribute

async def get_event_bonus_characters_id_jp(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_event_deck_bonuses_api_jp(session)
    characters_id_list = []
    for thing in event_api:
        if event_id == thing['eventId']:
            character_id = thing.get('gameCharacterUnitId')
            characters_id_list.append(character_id)
    if None in characters_id_list:
        characters_id_list.remove(None)
    characters_id_list = list(dict.fromkeys(characters_id_list))
    return characters_id_list

async def get_event_bonus_characters_name_jp(characters_id_list: list, session: aiohttp.ClientSession):
    characters_name_list = []
    event_api = await get_sekai_characters_info_api(session)
    for character_id in characters_id_list:
        for thing in event_api:
            if character_id == thing['id']:
                first_name = thing['firstName']
                last_name = thing['givenName']
                name = f'{first_name}{last_name}'
                characters_name_list.append(name)
    if None in characters_name_list:
        characters_name_list.remove(None)
    return characters_name_list   

#tw
async def get_current_event_id_tw(session: aiohttp.ClientSession):
    event_api = await get_sekai_world_events_api_tw(session)
    return event_api[-3]['id']

async def get_event_name_tw(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_events_api_tw(session)
    for thing in event_api:
        if event_id == thing['id']:
            event_name = thing['name']
            return event_name

async def get_event_type_tw(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_events_api_tw(session)
    for thing in event_api:
        if event_id == thing['id']:
            event_type = thing['eventType']
            return event_type

async def get_event_start_time_tw(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_events_api_tw(session)
    for thing in event_api:
        if event_id == thing['id']:
            event_start_time = thing['startAt']
            return event_start_time

async def get_event_end_time_tw(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_events_api_tw(session)
    for thing in event_api:
        if event_id == thing['id']:
            event_end_time = thing['aggregateAt']
            return event_end_time

async def get_event_bonus_attribute_tw(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_event_deck_bonuses_api_tw(session)
    for thing in event_api:
        if event_id == thing['eventId']:
            event_bonus_attribute = thing['cardAttr'].capitalize()
            return event_bonus_attribute
        
async def get_event_banner_name_tw(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_events_api_tw(session)
    for thing in event_api:
        if event_id == thing['id']:
            event_banner_name = thing['assetbundleName']
            return event_banner_name

async def get_event_bonus_characters_id_tw(event_id, session: aiohttp.ClientSession):
    event_api = await get_sekai_event_deck_bonuses_api_tw(session)
    characters_id_list = []
    for thing in event_api:
        if event_id == thing['eventId']:
            character_id = thing.get('gameCharacterUnitId')
            characters_id_list.append(character_id)
    if None in characters_id_list:
        characters_id_list.remove(None)
    characters_id_list = list(dict.fromkeys(characters_id_list))
    return characters_id_list

async def get_event_bonus_characters_name_tw(characters_id_list: list, session: aiohttp.ClientSession):
    characters_name_list = []
    event_api = await get_sekai_characters_info_api(session)
    for character_id in characters_id_list:
        for thing in event_api:
            if character_id == thing['id']:
                first_name = thing['firstName']
                last_name = thing['givenName']
                name = f'{first_name}{last_name}'
                characters_name_list.append(name)
    if None in characters_name_list:
        characters_name_list.remove(None)
    return characters_name_list   
