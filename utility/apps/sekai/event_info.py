#jp
async def get_current_event_id_jp():
    import re
    from utility.apps.sekai.api_functions import get_sekai_world_events_api_jp
    event_api = await get_sekai_world_events_api_jp()
    return event_api[-1]['id']

async def get_event_name_jp(event_id):
    from utility.apps.sekai.api_functions import get_sekai_events_api_jp
    event_api = await get_sekai_events_api_jp()
    event_name = event_api[-1]['name']
    return event_name

async def get_event_type_jp(event_id):
    from utility.apps.sekai.api_functions import get_sekai_events_api_jp
    event_api = await get_sekai_events_api_jp()
    event_name = event_api[-1]['eventType'].capitalize()
    return event_name

async def get_event_start_time_jp(event_id):
    from utility.apps.sekai.api_functions import get_sekai_events_api_jp
    event_start_time = event_api[-1]['startAt']
    return event_start_time

async def get_event_end_time_jp(event_id):
    from utility.apps.sekai.api_functions import get_sekai_events_api_jp
    event_api = await get_sekai_events_api_jp()
    event_end_time = event_api[-1]['aggregateAt']
    return event_end_time

async def get_event_banner_name_jp(event_id):
    from utility.apps.sekai.api_functions import get_sekai_events_api_jp
    event_api = await get_sekai_events_api_jp()
    event_banner_name = event_api[-1]['assetbundleName']
    return event_banner_name

async def get_event_bonus_attribute_jp():
    from utility.apps.sekai.api_functions import get_sekai_event_deck_bonuses_api_jp
    event_api = await get_sekai_event_deck_bonuses_api_jp()
    event_bonus_attribute = event_api[-1]['cardAttr'].capitalize()
    return event_bonus_attribute

async def get_event_bonus_characters_id_jp(event_id):
    from utility.apps.sekai.api_functions import get_sekai_event_deck_bonuses_api_jp
    event_api = await get_sekai_event_deck_bonuses_api_jp()
    characters_id_list = []
    for thing in event_api:
        if event_id == thing['eventId']:
            character_id = thing['gameCharacterUnitId']
            characters_id_list.append(character_id)
    return characters_id_list

#tw
async def get_current_event_id_tw():
    import re
    from utility.apps.sekai.api_functions import get_sekai_world_events_api_tw
    event_api = await get_sekai_world_events_api_tw()
    return event_api[-1]['id']

async def get_event_name_tw(event_id):
    from utility.apps.sekai.api_functions import get_sekai_events_api_tw
    event_api = await get_sekai_events_api_tw()
    event_name = event_api[-1]['name']
    return event_name

async def get_event_type_tw(event_id):
    from utility.apps.sekai.api_functions import get_sekai_events_api_tw
    event_api = await get_sekai_events_api_tw()
    event_name = event_api[-1]['eventType'].capitalize()
    return event_name

async def get_event_start_time_tw(event_id):
    from utility.apps.sekai.api_functions import get_sekai_events_api_tw
    event_api = await get_sekai_events_api_tw()
    event_start_time = event_api[-1]['startAt']
    return event_start_time

async def get_event_end_time_tw(event_id):
    from utility.apps.sekai.api_functions import get_sekai_events_api_tw
    event_api = await get_sekai_events_api_tw()
    event_end_time = event_api[-1]['aggregateAt']
    return event_end_time

async def get_event_banner_name_tw(event_id):
    from utility.apps.sekai.api_functions import get_sekai_events_api_tw
    event_api = await get_sekai_events_api_tw()
    event_banner_name = event_api[-1]['assetbundleName']
    return event_banner_name

async def get_event_bonus_attribute_tw():
    from utility.apps.sekai.api_functions import get_sekai_event_deck_bonuses_api_tw
    event_api = await get_sekai_event_deck_bonuses_api_tw()
    event_bonus_attribute = event_api[-1]['cardAttr'].capitalize()
    return event_bonus_attribute
