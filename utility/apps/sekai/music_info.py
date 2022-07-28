#musics
async def get_music_title(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for thing in music_api:
        thing_id = thing['id']
        if music_id == thing_id:
            music_title = thing['title']
            return music_title

async def get_music_lyricist(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for thing in music_api:
        thing_id = thing['id']
        if music_id == thing_id:
            music_lyricist = thing['lyricist']
            return music_lyricist

async def get_music_composer(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for thing in music_api:
        thing_id = thing['id']
        if music_id == thing_id:
            music_composer = thing['composer']
            return music_composer

async def get_music_arranger(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for thing in music_api:
        thing_id = thing['id']
        if music_id == thing_id:
            music_arranger = thing['arranger']
            return music_arranger
        
async def get_music_published_time(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for thing in music_api:
        thing_id = thing['id']
        if music_id == thing_id:
            music_published_time = thing['publishedAt']
            return music_published_time    
    
'''
async def get_music_asset_name(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    music_asset_name = music_api[music_id-1]['assetbundleName']
    return music_asset_name
'''
#music_difficulties
async def get_music_difficulty_easy_difficulty(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
            difficulty = thing['musicDifficulty'].capitalize()
            return difficulty

async def get_music_difficulty_easy_level(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    level = music_api[music_id-1]['playLevel']
    return level

async def get_music_difficulty_easy_note_count(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    note_count = music_api[music_id-1]['noteCount']
    return note_count

async def get_music_difficulty_normal_difficulty(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    difficulty = music_api[music_id]['musicDifficulty'].capitalize()
    return difficulty

async def get_music_difficulty_normal_level(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    level = music_api[music_id]['playLevel']
    return level

async def get_music_difficulty_normal_note_count(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    note_count = music_api[music_id]['noteCount']
    return note_count

async def get_music_difficulty_hard_difficulty(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    difficulty = music_api[music_id+1]['musicDifficulty'].capitalize()
    return difficulty

async def get_music_difficulty_hard_level(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    level = music_api[music_id+1]['playLevel']
    return level

async def get_music_difficulty_hard_note_count(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    note_count = music_api[music_id+1]['noteCount']
    return note_count

async def get_music_difficulty_expert_difficulty(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    difficulty = music_api[music_id+2]['musicDifficulty'].capitalize()
    return difficulty

async def get_music_difficulty_expert_level(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    level = music_api[music_id+2]['playLevel']
    return level

async def get_music_difficulty_expert_note_count(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    note_count = music_api[music_id+2]['noteCount']
    return note_count

async def get_music_difficulty_master_difficulty(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    difficulty = music_api[music_id+3]['musicDifficulty'].capitalize()
    return difficulty

async def get_music_difficulty_master_level(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    level = music_api[music_id+3]['playLevel']
    return level

async def get_music_difficulty_master_note_count(music_id):
    from utility.apps.sekai.api_functions import get_sekai_music_difficulties_api
    music_api = await get_sekai_music_difficulties_api()
    note_count = music_api[music_id+3]['noteCount']
    return note_count

