import aiohttp

from utility.apps.sekai.api_functions import (get_sekai_user_api, get_sekai_cards_info_api, get_sekai_characters_info_api)

#json
async def get_user_game_data(import_id: int, path: str, session: aiohttp.ClientSession):
    api = await get_sekai_user_api(import_id, session)
    path_list = ['userId', 'name', 'deck', 'rank']
    if path in path_list:
        result = api['user']['userGamedata'][path]
        return result    

async def get_user_profile(import_id: int, path: str, session: aiohttp.ClientSession):
    api = await get_sekai_user_api(import_id, session)
    path_list = ['userId', 'word', 'twitterId', 'profileImageType']
    if path in path_list:
        result = api['userProfile'][path]
        return result    
    
async def get_user_decks(import_id: int, path: str, session: aiohttp.ClientSession):
    api = await get_sekai_user_api(import_id, session)
    path_list = ['leader', 'subLeader', 'member1', 'member2', 'member3', 'member4', 'member5' ]
    if path in path_list:
        result = api['userDecks'][0][path]
        return result    


async def get_user_cards(import_id: int, index: int, path: str, session: aiohttp.ClientSession):
    api = await get_sekai_user_api(import_id, session)
    path_list = ['cardId', 'level', 'masterRank', 'specialTraningStatus', 'defaultImage']
    if path in path_list:
        result = api['userCards'][index][path]
        return result    

#img
async def get_user_profile_pic(import_id: int, card_id: int, session: aiohttp.ClientSession):
    api = await get_sekai_cards_info_api(session)
    for card in api:
        if card['id'] == card_id:
            asset_bundle_name = card.get('assetbundleName')
            
    status_convert = {
        'original': 'normal',
        'special_training': 'after_training'
    }
    
    status = await get_user_cards(import_id, 0, 'defaultImage', session)
    status = status_convert[status]

    img_url = f'https://asset.pjsekai.moe/startapp/thumbnail/chara/{asset_bundle_name}_{status}.png'
    
    return img_url

async def get_profile_img(card_id: int, session: aiohttp.ClientSession):
    api = await get_sekai_cards_info_api(session)
    api2 = await get_sekai_characters_info_api(session)
    for card in api:
        if card['id'] == card_id:
            character_id = card.get('characterId')
            support_unit = card.get('supportUnit') 
            if support_unit == 'none': 
                for char in api2:
                    if char['id'] == character_id: 
                        unit = char.get('unit')
                    else: 
                        unit = '404 Not Found' 
            else:       
                unit = support_unit
    
    path_convert= {
        'light_sound': 'img_story_kyoshitsu',
        'school_refusal': 'img_story_daremoinai',
        'idol': 'img_story_stage',
        'street': 'img_story_street',
        'theme_park': 'img_story_wonderLand'
    }
    
    path = path_convert[unit]
    
    url =  f'https://gitlab.com/pjsekai/sprites/-/raw/master/{path}.png'
    
    return url
    