# song embed
# musics
import aiohttp
from utility.apps.sekai.api_functions import (get_sekai_music_difficulties_api,
                                              get_sekai_music_tags_api,
                                              get_sekai_musics_api)
from utility.utils import defaultEmbed
from utility.apps.sekai.time_formatting import format_date_jp
#music_info
async def get_music_info(music_id: int, info_type: str, session: aiohttp.ClientSession):
    music_api = await get_sekai_musics_api(session)
    for thing in music_api:
        thing_id = thing['id']
        if music_id == thing_id:
            music_info = thing[f'{info_type}']
            return music_info

# music_difficulties
async def get_music_difficulty_info(music_id: int, info_type: str, difficulty: str, session: aiohttp.ClientSession):
    music_api = await get_sekai_music_difficulties_api(session)
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == f'{difficulty}':
            music_difficulty_info = str(thing[f'{info_type}']).capitalize()
            return music_difficulty_info

# tags
async def get_group_music(group: str, session: aiohttp.ClientSession):
    music_api = await get_sekai_music_tags_api(session)
    group_music_embed_list = []
    for thing in music_api:
        if thing['musicTag'] == f'{group}':
            music_id = thing['musicId']

            music_title = await get_music_info(music_id, 'title', session)
            music_lyricist = await get_music_info(music_id, 'lyricist', session)
            music_composer = await get_music_info(music_id, 'composer', session)
            music_arranger = await get_music_info(music_id, 'arranger', session)
            music_published_time = await format_date_jp(await get_music_info(music_id, 'publishedAt', session))

            easy_difficulty = await get_music_difficulty_info(music_id, 'musicDifficulty', 'easy', session)
            easy_level = await get_music_difficulty_info(music_id, 'playLevel', 'easy', session)
            easy_note_count = await get_music_difficulty_info(music_id, 'noteCount', 'easy', session)

            normal_difficulty = await get_music_difficulty_info(music_id, 'musicDifficulty', 'normal', session)
            normal_level = await get_music_difficulty_info(music_id, 'playLevel', 'normal', session)
            normal_note_count = await get_music_difficulty_info(music_id, 'noteCount', 'normal', session)
            
            hard_difficulty = await get_music_difficulty_info(music_id, 'musicDifficulty', 'hard', session)
            hard_level = await get_music_difficulty_info(music_id, 'playLevel', 'hard', session)
            hard_note_count = await get_music_difficulty_info(music_id, 'noteCount', 'hard', session)
            
            expert_difficulty = await get_music_difficulty_info(music_id, 'musicDifficulty', 'expert', session)
            expert_level = await get_music_difficulty_info(music_id, 'playLevel', 'expert', session)
            expert_note_count = await get_music_difficulty_info(music_id, 'noteCount', 'expert', session)
            
            master_difficulty = await get_music_difficulty_info(music_id, 'musicDifficulty', 'master', session)
            master_level = await get_music_difficulty_info(music_id, 'playLevel', 'master', session)
            master_note_count = await get_music_difficulty_info(music_id, 'noteCount', 'master', session)
            
            if len(str(music_id)) == 1:
                music_asset_name = f'jacket_s_00{music_id}'
            elif len(str(music_id)) == 2:
                music_asset_name = f'jacket_s_0{music_id}'
            elif len(str(music_id)) == 3:
                music_asset_name = f'jacket_s_{music_id}'

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
            
            group_music_embed_list.append(embed)
            
    return group_music_embed_list
