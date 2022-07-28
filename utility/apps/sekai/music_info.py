#musics
async def get_music_title(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    count = -1
    global music_title
    music_title = ''
    for ids in music_api:
        count = ids + 1
        return count
    if music_api[int(count)]['id'] == music_id:
        music_title = [int(count)]['title']
    return music_title

async def get_music_lyricist(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    count = -1
    global music_lyricist
    music_lyricist = ''
    for ids in music_api:
        count + 1
        if music_api[count]['id'] == music_id:
            music_lyricist = music_api[count]['lyricist']
    return music_lyricist

async def get_music_composer(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    count = -1
    global music_composer
    music_composer = ''
    for ids in music_api:
        count + 1
        if music_api[count]['id'] == music_id:
            music_composer = music_api[count]['composer']
    return music_composer

async def get_music_arranger(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    count = -1
    global music_arranger
    music_arranger = ''
    for ids in music_api:
        count + 1
        if music_api[count]['id'] == music_id:
            music_arranger = music_api[count]['arranger']
    return music_arranger

async def get_music_published_time(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    count = -1
    global music_published_time
    music_published_time = 0
    for ids in music_api:
        count + 1
        if music_api[count]['id'] == music_id:
            music_published_time = music_api[count]['publishedAt']
    return music_published_time

async def get_music_asset_name(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    count = -1
    global music_asset_name
    music_asset_name = ''
    for ids in music_api:
        count + 1
        if music_api[count]['id'] == music_id:
            music_asset_name = music_api[count]['assetbundleName']
    return music_asset_name
#music_difficulties

#music_vocals