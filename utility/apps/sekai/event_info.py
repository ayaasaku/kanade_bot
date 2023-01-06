import time
import aiohttp

from utility.apps.sekai.api_functions import (
    get_sekai_characters_info_api, get_sekai_event_deck_bonuses_api_jp,
    get_sekai_event_deck_bonuses_api_tw, get_sekai_events_api_jp,
    get_sekai_events_api_tw)

async def get_event_info(session: aiohttp.ClientSession, type: str):
    if type == 'jp':
        event_api = await get_sekai_events_api_jp(session)
    else:
        event_api = await get_sekai_events_api_tw(session)
        
    for thing in event_api:
        event_start_time = thing['startAt']
        event_end_time = thing['aggregateAt']
        current_time = int(time.time())
        current_time *= 1000
        async def find_event_info(info):  
            return thing[f'{info}']   

        if current_time >= event_start_time and current_time <= event_end_time: 
            event_id = await find_event_info('id')
            event_name = await find_event_info('name')
            event_type = await find_event_info('eventType')
            event_start_time = await find_event_info('startAt')
            event_start_time //= 1000
            event_end_time = await find_event_info('aggregateAt')
            event_end_time //= 1000
            event_banner_name = await find_event_info('assetbundleName')
            
            if type == 'tw':
                api = await get_sekai_event_deck_bonuses_api_tw(session) 
            elif type == 'jp':
                api = await get_sekai_event_deck_bonuses_api_jp(session)
                
            characters_id_list = []
            for i in api:
                if event_id == i['eventId']:
                    character_id = i.get('gameCharacterUnitId')
                    event_bonus_attribute = i.get('cardAttr')
                    characters_id_list.append(character_id)
            if None in characters_id_list:
                characters_id_list.remove(None)
            characters_id_list = list(dict.fromkeys(characters_id_list))
            
            characters_name_list = []
            api = await get_sekai_characters_info_api(session)
            for character_id in characters_id_list:
                for character in api:
                    if character_id == character['id']:
                        first_name = character['firstName']
                        last_name = character['givenName']
                        name = f'{first_name}{last_name}'
                        characters_name_list.append(name)
            if None in characters_name_list:
                characters_name_list.remove(None)
                
            else:
                event_info = {
                    'event_id': event_id,
                    'event_name': event_name,
                    'event_type': event_type.capitalize(),
                    'event_start_time': event_start_time,
                    'event_end_time': event_end_time,
                    'event_banner_name': event_banner_name,
                    'event_bonus_attribute': event_bonus_attribute.capitalize(),
                    'characters_name_list': characters_name_list        
                }
        else: 
            event_info = None 
            
    return event_info
            
