# song embed
# musics
import aiohttp
from utility.apps.sekai.api_functions import (get_sekai_music_difficulties_api,
                                              get_sekai_music_tags_api,
                                              get_sekai_musics_api)
from utility.utils import defaultEmbed


async def get_music_title(music_id: int, session: aiohttp.ClientSession):
    music_api = await get_sekai_musics_api(session)
    for thing in music_api:
        thing_id = thing['id']
        if music_id == thing_id:
            music_title = thing['title']
            return music_title


async def get_music_lyricist(music_id):
    music_api = await get_sekai_musics_api()
    for thing in music_api:
        thing_id = thing['id']
        if music_id == thing_id:
            music_lyricist = thing['lyricist']
            return music_lyricist


async def get_music_composer(music_id):
    music_api = await get_sekai_musics_api()
    for thing in music_api:
        thing_id = thing['id']
        if music_id == thing_id:
            music_composer = thing['composer']
            return music_composer


async def get_music_arranger(music_id):
    music_api = await get_sekai_musics_api()
    for thing in music_api:
        thing_id = thing['id']
        if music_id == thing_id:
            music_arranger = thing['arranger']
            return music_arranger


async def get_music_published_time(music_id):
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
    return music_asset_name
'''
# music_difficulties


async def get_music_difficulty_easy_difficulty(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
            difficulty = thing['musicDifficulty'].capitalize()
            return difficulty


async def get_music_difficulty_easy_level(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
            level = thing['playLevel']
            return level

    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
            note_count = thing['noteCount']
            return note_count


async def get_music_difficulty_normal_difficulty(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'normal':
            difficulty = thing['musicDifficulty'].capitalize()
            return difficulty


async def get_music_difficulty_normal_level(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'normal':
            level = thing['playLevel']


async def get_music_difficulty_normal_note_count(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'normal':
            return note_count


async def get_music_difficulty_hard_difficulty(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        difficulty = thing['musicDifficulty'].capitalize()
        return difficulty


async def get_music_difficulty_hard_level(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'hard':
            level = thing['playLevel']
            return level


async def get_music_difficulty_hard_note_count(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'hard':
            note_count = thing['noteCount']
            return note_count


async def get_music_difficulty_expert_difficulty(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'expert':
            difficulty = thing['musicDifficulty'].capitalize()
            return difficulty

    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'expert':
            level = thing['playLevel']
            return level


async def get_music_difficulty_expert_note_count(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'expert':
            note_count = thing['noteCount']
            return note_count


async def get_music_difficulty_master_difficulty(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'master':
            difficulty = thing['musicDifficulty'].capitalize()
            return difficulty
            level = thing['playLevel']
            return level


async def get_music_difficulty_master_note_count(music_id):
    music_api = await get_sekai_music_difficulties_api()
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'master':
            note_count = thing['noteCount']
            return note_count

# get song embed


async def get_song_embed(import_id: int, session: aiohttp.ClientSession):
    from utility.apps.sekai.music_info import (
        get_music_arranger, get_music_composer,
        get_music_difficulty_easy_difficulty, get_music_difficulty_easy_level,
        get_music_difficulty_easy_note_count,
        get_music_difficulty_expert_difficulty,
        get_music_difficulty_expert_level,
        get_music_difficulty_expert_note_count,
        get_music_difficulty_hard_difficulty, get_music_difficulty_hard_level,
        get_music_difficulty_hard_note_count,
        get_music_difficulty_master_difficulty,
        get_music_difficulty_master_level,
        get_music_difficulty_master_note_count,
        get_music_difficulty_normal_difficulty,
        get_music_difficulty_normal_level,
        get_music_difficulty_normal_note_count, get_music_lyricist,
        get_music_published_time, get_music_tags, get_music_title)
    from utility.apps.sekai.time_formatting import format_date

    global music_id
    music_id = import_id

    music_title = await get_music_title(music_id, session)
    music_lyricist = await get_music_lyricist(music_id)
    music_composer = await get_music_composer(music_id)
    music_arranger = await get_music_arranger(music_id)
    music_published_time = await format_date(await get_music_published_time(music_id))
    if len(str(music_id)) == 1:
        music_asset_name = f'jacket_s_00{music_id}'
    elif len(str(music_id)) == 2:
        music_asset_name = f'jacket_s_0{music_id}'
    elif len(str(music_id)) == 3:
        music_asset_name = f'jacket_s_{music_id}'

    easy_difficulty = await get_music_difficulty_easy_difficulty(music_id)
    easy_level = await get_music_difficulty_easy_level(music_id)
    easy_note_count = await get_music_difficulty_easy_note_count(music_id)

    normal_difficulty = await get_music_difficulty_normal_difficulty(music_id)
    normal_level = await get_music_difficulty_normal_level(music_id)
    normal_note_count = await get_music_difficulty_normal_note_count(music_id)

    hard_difficulty = await get_music_difficulty_hard_difficulty(music_id)
    hard_level = await get_music_difficulty_hard_level(music_id)
    hard_note_count = await get_music_difficulty_hard_note_count(music_id)

    expert_difficulty = await get_music_difficulty_expert_difficulty(music_id)
    expert_level = await get_music_difficulty_expert_level(music_id)
    expert_note_count = await get_music_difficulty_expert_note_count(music_id)

    master_difficulty = await get_music_difficulty_master_difficulty(music_id)
    master_level = await get_music_difficulty_master_level(music_id)
    master_note_count = await get_music_difficulty_master_note_count(music_id)

    music_tag = await get_music_tags(music_id)

    cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
    music_url = f'https://sekai.best/music/{music_id}'

    embed = defaultEmbed(title=f'**{music_title}**')
    embed.set_thumbnail(url=cover_url)
    embed.add_field(name='作詞', value=music_lyricist, inline=True)
    embed.add_field(name='作曲', value=music_composer, inline=True)
    embed.add_field(name='編曲', value=music_arranger, inline=True)
    embed.add_field(name='發佈時間', value=music_published_time, inline=False)
    embed.add_field(name='\u200b', value='**難度**', inline=False)
    embed.add_field(name=easy_difficulty,
                    value=f'等級：{easy_level}\n音符數量：{easy_note_count}', inline=True)
    embed.add_field(name=normal_difficulty,
                    value=f'等級：{normal_level}\n音符數量：{normal_note_count}', inline=True)
    embed.add_field(name=hard_difficulty,
                    value=f'等級：{hard_level}\n音符數量：{hard_note_count}', inline=True)
    embed.add_field(name=expert_difficulty,
                    value=f'等級：{expert_level}\n音符數量：{expert_note_count}', inline=True)
    embed.add_field(name=master_difficulty,
                    value=f'等級：{master_level}\n音符數量：{master_note_count}\n\u200b', inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline=True)
    embed.add_field(name='更多資訊', value=music_url, inline=False)
    embed.add_field(name='type', value=music_tag, inline=False)
    return embed
# tags


async def get_vocaloid_music(session: aiohttp.ClientSession):
    music_api = await get_sekai_music_tags_api()
    vocaloid_music_embed_list = []
    for thing in music_api:
        if music_tag == 'vocaloid':
            music_id = thing['musicId']
            embed = await get_song_embed(music_id, session)
            vocaloid_music_embed_list.append(embed)
    if None in vocaloid_music_embed_list:
        vocaloid_music_embed_list.remove(None)
    return vocaloid_music_embed_list


async def get_light_music_club_music():
    music_api = await get_sekai_music_tags_api()
    light_music_club_music_embed_list = []
    for thing in music_api:
        if music_tag == 'light_music_club':
            music_id = thing['musicId']
            embed = get_song_embed(music_id)
            light_music_club_music_embed_list.append(embed)
    if None in light_music_club_music_embed_list:
        light_music_club_music_embed_list.remove(None)
    return light_music_club_music_embed_list


async def get_idol_music():
    music_api = await get_sekai_music_tags_api()
    idol_music_embed_list = []
    for thing in music_api:
        if music_tag == 'idol':
            music_id = thing['musicId']
            embed = get_song_embed(music_id)
            idol_music_embed_list.append(embed)
    if None in idol_music_embed_list:
        idol_music_embed_list.remove(None)
    return idol_music_embed_list


async def get_street_music():
    music_api = await get_sekai_music_tags_api()
    street_music_embed_list = []
    for thing in music_api:
        if music_tag == 'street':
            music_id = thing['musicId']
            embed = get_song_embed(music_id)
            street_music_embed_list.append(embed)
    if None in street_music_embed_list:
        street_music_embed_list.remove(None)
    return street_music_embed_list


async def get_theme_park_music():
    music_api = await get_sekai_music_tags_api()
    theme_park_music_embed_list = []
    for thing in music_api:
        if music_tag == 'street':
            music_id = thing['musicId']
            embed = get_song_embed(music_id)
            theme_park_music_embed_list.append(embed)
    if None in theme_park_music_embed_list:
        theme_park_music_embed_list.remove(None)
    return theme_park_music_embed_list


async def get_school_refusal_music():
    music_api = await get_sekai_music_tags_api()
    school_refusal_music_embed_list = []
    for thing in music_api:
        if music_tag == 'street':
            music_id = thing['musicId']
            embed = get_song_embed(music_id)
            school_refusal_music_embed_list.append(embed)
    if None in school_refusal_music_embed_list:
        school_refusal_music_embed_list.remove(None)
    return school_refusal_music_embed_list
