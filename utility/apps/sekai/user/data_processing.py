import aiohttp
import time
from utility.apps.sekai.api_functions import (get_sekai_area_items_level_info_api, get_sekai_cards_info_api,
                                              get_sekai_characters_info_api,
                                              get_sekai_user_api,
                                              get_sekai_area_items_info_api,
                                              get_sekai_area_items_level_info_api,
                                              get_sekai_virtual_live_api_tw,
                                              get_sekai_virtual_live_api_jp,
                                              get_sekai_musics_api,
                                              get_sekai_music_tags_api)
from data.channel_list import channel_list
from utility.utils import defaultEmbed

#json
async def get_user_game_data(import_id: str, path: str, session: aiohttp.ClientSession):
    api = await get_sekai_user_api(import_id, session)
    path_list = ['userId', 'name', 'deck', 'rank']
    if path in path_list:
        result = api['user']['userGamedata'][path]
        return result    

async def get_user_profile(import_id: str, path: str, session: aiohttp.ClientSession):
    api = await get_sekai_user_api(import_id, session)
    path_list = ['userId', 'word', 'twitterId', 'profileImageType']
    if path in path_list:
        result = api['userProfile'][path]
        return result    
    
async def get_user_decks(import_id: str, path: str, session: aiohttp.ClientSession):
    api = await get_sekai_user_api(import_id, session)
    path_list = ['leader', 'subLeader', 'member1', 'member2', 'member3', 'member4', 'member5' ]
    if path in path_list:
        result = api['userDecks'][0][path]
        return result    

async def get_user_area_items(import_id: str, session: aiohttp.ClientSession):
    api = await get_sekai_user_api(import_id, session)
    api2 = await get_sekai_area_items_info_api(session)
    api3 = await get_sekai_area_items_level_info_api(session)
    embed_list = []
    area_items = api['userAreaItems']
    for item in area_items:
        item_id = item['areaItemId']
        item_level = item['level']
        for thing in api3:
            if item_id == thing['areaItemId'] and item_level == thing['level']:
                sentence = thing['sentence']
                #format sentence
                if sentence.count('。') == 1:
                    part1, part2 = sentence.split('<color=')
                    part2_1, part2_2 = part2.split('">')
                    part2_2_1, part2_2_2 = part2_2.split('</color')
                    sentence = f'{part1}{part2_2_1}。'
                    
                elif sentence.count('。') == 2:
                    sentence = sentence.rstrip(sentence[-1])
                    part1, part2 = sentence.split('>。')
                    
                    part1_1, part1_2 = part1.split('<color=')
                    part1_2_1, part1_2_2 = part1_2.split('">')
                    part1_2_2_1, part1_2_2_2 = part1_2_2.split('</color')
                    sentence1 = f'{part1_1}{part1_2_2_1}。'
                    
                    part2_1, part2_2 = part2.split('<color=')
                    part2_2_1, part2_2_2 = part2_2.split('">')
                    part2_2_2_1, part2_2_2_2 = part2_2_2.split('</color')
                    sentence2 = f'{part2_1}{part2_2_2_1}。'
                    
                    sentence = f'{sentence1}\n{sentence2}'
                    
        for thing in api2:
            if item_id == thing['id']:
                name = thing['name']
                asset_bundle_name = thing['assetbundleName']
                img = f'https://storage.sekai.best/sekai-assets/areaitem/{asset_bundle_name}_rip/{asset_bundle_name}.webp'
                embed = defaultEmbed(title=name, description= f'**等級：{item_level}**\n{sentence}')
                embed.set_thumbnail(url=img)
        embed_list.append(embed)        
    return embed_list
        

async def get_user_cards(import_id: str, index, path: str, session: aiohttp.ClientSession):
    api = await get_sekai_user_api(import_id, session)
    path_list = ['cardId', 'level', 'masterRank', 'specialTraningStatus', 'defaultImage']
    if index == None:
        result = api['userCards']
    elif path in path_list and index != None:
            result = api['userCards'][index][path]
    return result    

#img
async def get_user_profile_pic(import_id: str, card_id: int, session: aiohttp.ClientSession):
    api = await get_sekai_cards_info_api(session)
    for card in api:
        if card['id'] == card_id:
            asset_bundle_name = card.get('assetbundleName')
            
    status_convert = {
        'original': 'normal',
        'special_training': 'after_training'
    }
    
    cards = await get_user_cards(import_id, None, 'N/A', session)
    for card in cards:
        if card_id == card['cardId']:
            default_image = card['defaultImage']
    status = status_convert[default_image]

    img_url = f'https://asset.pjsekai.moe/startapp/thumbnail/chara/{asset_bundle_name}_{status}.png'
    
    return img_url

async def get_profile_img(card_id: int, session: aiohttp.ClientSession):
    api = await get_sekai_cards_info_api(session)
    api2 = await get_sekai_characters_info_api(session)
    for card in api:
        if card['id'] == card_id:
            character_id = card['characterId']
            support_unit = card['supportUnit'] 
            if support_unit == 'none': 
                for char in api2:
                    if char['id'] == character_id: 
                        unit = char['unit']
            else:       
                unit = support_unit
    
    path_convert= {
        'light_sound': 'img_story_kyoshitsu',
        'school_refusal': 'img_story_daremoinai',
        'idol': 'img_story_stage',
        'street': 'img_story_street',
        'theme_park': 'img_story_wonderLand'
    }
    
    if unit == 'piapro':
        return None
    path = path_convert[unit]
    
    url =  f'https://gitlab.com/pjsekai/sprites/-/raw/master/{path}.png'
    
    return url
    
#character level
async def get_user_character_level(import_id: str, session: aiohttp.ClientSession):
    api = await get_sekai_user_api(import_id, session)
    result = api['userCharacters']
    return result    

async def get_current_virtual_live(server: str, session: aiohttp.ClientSession):
    if server == 'tw':
        api = await get_sekai_virtual_live_api_tw(session)
    elif server == 'jp':
        api = await get_sekai_virtual_live_api_jp(session)
    for live in api:
        virtual_live_start_time = live['startAt']
        virtual_live_end_time = live['endAt']
        current_time = time.time()
        if current_time > virtual_live_start_time and current_time < virtual_live_end_time:
            current_virtual_live = live
            return current_virtual_live   
        else:
            return None
        
     
async def virtual_live_ping_tw(bot, session: aiohttp.ClientSession):
    current_virtual_live = await get_current_virtual_live('tw', session)
    if current_virtual_live != None:
        for thing in current_virtual_live['virtualLiveSchedules']:
            name = current_virtual_live['name']
            virtual_live_start_time = thing['startAt']
            current_time = time.time()
            if current_time >= (virtual_live_start_time - 310) and current_time < virtual_live_start_time:
                embed = defaultEmbed(title= f'虛擬 Live 即將開始', description=f'{name} 將於五分鐘後開始')
                for i in channel_list:           
                    channel = bot.get_channel(i)
                    await channel.send(embed=embed)

async def virtual_live_ping_jp(bot, session: aiohttp.ClientSession):
    current_virtual_live = await get_current_virtual_live('jp', session)
    if current_virtual_live != None:
        for thing in current_virtual_live['virtualLiveSchedules']:
            name = current_virtual_live['name']
            virtual_live_start_time = thing['startAt']
            current_time = time.time()
            if current_time >= (virtual_live_start_time - 310) and current_time < virtual_live_start_time:
                embed = defaultEmbed(title= f'虛擬 Live 即將開始', description=f'{name} 將於五分鐘後開始')
                for i in channel_list:           
                    channel = bot.get_channel(i)
                    await channel.send(embed=embed)

   
async def get_group_music(session: aiohttp.ClientSession):
    music_tag_api = await get_sekai_music_tags_api(session)
    music_api = await get_sekai_musics_api(session)
    group_list = ['vocaloid', 'light_music_club', 'school_refusal', 'idol', 'street', 'theme_park', 'other']
    all_music = {
        'vocaloid': [],
        'light_music_club': [],
        'school_refusal': [],
        'idol': [],
        'street': [],
        'theme_park': [],
        'other': []
    }
   
    for group in group_list:
        for thing in music_tag_api:
            if thing['musicTag'] == f'{group}':
                music_id = thing['musicId']  
                for music in music_api:
                    if music_id == music['id']:
                        music_name = music['title']
                all_music[f'{group}'].append([music_name, music_id]) 
    return all_music
         
async def get_user_music(import_id: str, music_id: str, session: aiohttp.ClientSession):
    user_api = await get_sekai_user_api(import_id, session)
    music_api = await get_sekai_musics_api(session)
    api = user_api['userMusics']
    empty_list = []
    embed_list = []
    for music in music_api:
        if int(music_id) == music['id']:
            music_name = music['title']
    for music in api:
        if int(music_id) == music['musicId']:
            #embed = get_music_embed(music_id, session)
            for difficulty in music['userMusicDifficultyStatuses']:
                difficulty_name = difficulty['musicDifficulty']
                
                if len(music_id) == 1:
                    music_asset_name = f'jacket_s_00{music_id}'
                elif len(music_id) == 2:
                    music_asset_name = f'jacket_s_0{music_id}'
                elif len(music_id) == 3:
                    music_asset_name = f'jacket_s_{music_id}'
                    
                cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
                    
                if difficulty['userMusicResults'] == empty_list:
                    embed = defaultEmbed(title=f'**{music_name} - {difficulty_name.title()} - 尚未挑戰**', description=f'你尚未挑戰此難度')
                    embed.set_thumbnail(url=cover_url)
                    embed_list.append(embed)
                else:
                    embed = defaultEmbed(title=f'**{music_name} - {difficulty_name.title()}**')
                    embed_list.append(embed)
                    
                    for thing in difficulty['userMusicResults']:
                        if thing['playType'] == 'solo': play_type ='單人' 
                        elif thing['playType'] == 'multi': play_type ='多人' 
                        
                        score = thing['highScore']
                        full_combo = thing['fullComboFlg']
                        full_perfect = thing['fullPerfectFlg']
                        
                        embed.set_thumbnail(url=cover_url)
                        embed.add_field(name='\u200b', value=f'**{play_type}**', inline=False)
                        embed.add_field(name=f'最高分數',
                                        value=f'{score}', inline=False)
                        
                        if full_combo == True:
                            embed.add_field(name=f'Full Combo',
                                            value=f'<:tick:1024576420606918656>', inline=True)
                        elif full_combo == False:
                            embed.add_field(name=f'Full Combo',
                                            value=f'<:crosss:1024577482290114630> ', inline=True)
                            
                        if full_perfect == True:
                            embed.add_field(name=f'Full Perfect',
                                            value=f'<:tick:1024576420606918656>', inline=True)
                        elif full_perfect == False:
                            embed.add_field(name=f'Full Perfect',
                                            value=f'<:crosss:1024577482290114630> ', inline=True)
            return embed_list
                

    