# song embed
# musics
import aiohttp
from utility.apps.sekai.api_functions import (get_sekai_music_difficulties_api,
                                              get_sekai_music_tags_api,
                                              get_sekai_musics_api)
from utility.utils import defaultEmbed
from utility.apps.sekai.time_formatting import format_date_jp


#music_info
async def get_music_info(self, music_id: int, session: aiohttp.ClientSession):
    music_api = await get_sekai_musics_api(session)
    for thing in music_api:
        if music_id == thing['id']:
            music_title = thing['title']
            music_lyricist = thing['lyricist']
            music_composer = thing['composer']
            music_arranger = thing['arranger']
            music_published_time = await format_date_jp(thing['publishedAt'])
            music_info = [music_title, music_lyricist, music_composer, music_arranger, music_published_time]
            return music_info

# music_difficulties
async def get_music_difficulty_info(music_id: int, session: aiohttp.ClientSession):
    music_api = await get_sekai_music_difficulties_api(session)
    for thing in music_api:
        if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
            easy_level = thing['playLevel']
            easy_note_count = thing['noteCount']
            
            normal_level = thing['playLevel']
            normal_note_count = thing['noteCount']
            
            hard_level = thing['playLevel']
            hard_note_count = thing['noteCount']
            
            expert_level = thing['playLevel']
            expert_note_count = thing['noteCount']
            
            master_level = thing['playLevel']
            master_note_count = thing['noteCount']
            
            music_difficulty_info = [
                easy_level, easy_note_count, 
                normal_level, normal_note_count, 
                hard_level, hard_note_count, 
                expert_level, expert_note_count, 
                master_level, master_note_count
                ]
            return music_difficulty_info

# tags
async def get_group_music(group: str, session: aiohttp.ClientSession):
    music_api = await get_sekai_music_tags_api(session)
    group_music_embed_list = []
    for thing in music_api:
        if thing['musicTag'] == f'{group}':
            music_id = thing['musicId']

            info = await get_music_info(music_id, session)
            difficulty = await get_music_difficulty_info(music_id, session)

            if len(str(music_id)) == 1:
                music_asset_name = f'jacket_s_00{music_id}'
            elif len(str(music_id)) == 2:
                music_asset_name = f'jacket_s_0{music_id}'
            elif len(str(music_id)) == 3:
                music_asset_name = f'jacket_s_{music_id}'

            cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
            music_url = f'https://sekai.best/music/{music_id}'

            embed = defaultEmbed(title=f'**{info[0]}**')
            embed.set_thumbnail(url=cover_url)
            embed.add_field(name='作詞', value=info[1], inline=True)
            embed.add_field(name='作曲', value=info[2], inline=True)
            embed.add_field(name='編曲', value=f'{info[3]}\n\u200b', inline=True)
            embed.add_field(name='發佈時間', value=info[4], inline=False)
            embed.add_field(name='\u200b', value='**難度**', inline=False)
            embed.add_field(name='Easy',
                            value=f'等級：{difficulty[0]}\n音符數量：{difficulty[1]}', inline=True)
            embed.add_field(name='Normal',
                            value=f'等級：{difficulty[2]}\n音符數量：{difficulty[3]}', inline=True)
            embed.add_field(name='Hard',
                            value=f'等級：{difficulty[4]}\n音符數量：{difficulty[5]}', inline=True)
            embed.add_field(name='Expert',
                            value=f'等級：{difficulty[6]}\n音符數量：{difficulty[7]}', inline=True)
            embed.add_field(name='Master',
                            value=f'等級：{difficulty[8]}\n音符數量：{difficulty[9]}\n\u200b', inline=True)
            embed.add_field(name='\u200b', value='\u200b', inline=True)
            embed.add_field(name='更多資訊', value=music_url, inline=False)
            
            group_music_embed_list.append(embed)
            
    return group_music_embed_list