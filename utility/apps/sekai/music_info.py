#musics
async def get_music_title(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for ids in music_api:
        if music_api[ids]['id'] == music_id:
            music_title = [ids]['title']
    return music_title

async def get_music_lyricist(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for ids in music_api:
        if music_api[ids]['id'] == music_id:
            music_title = music_api[ids]['lyricist']
    return music_lyricist

async def get_music_composer(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for ids in music_api:
        if music_api[ids]['id'] == music_id:
            music_composer =music_api[ids]['composer']
    return music_composer

async def get_music_arranger(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for ids in music_api:
        if music_api[ids]['id'] == music_id:
            music_arranger = music_api[ids]['arranger']
    return music_arranger

async def get_music_published_time(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for ids in music_api:
        if music_api[ids]['id'] == music_id:
            music_published_time = music_api[ids]['publishedAt']
    return music_published_time

async def get_music_asset_name(music_id):
    from utility.apps.sekai.api_functions import get_sekai_musics_api
    music_api = await get_sekai_musics_api()
    for ids in music_api:
        if music_api[ids]['id'] == music_id:
            music_asset_name = music_api[ids]['assetbundleName']
    return music_asset_name
#music_difficulties

#music_vocals