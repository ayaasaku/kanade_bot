import aiohttp
from utility.apps.sekai.api_functions import (get_sekai_music_difficulties_api,
                                              get_sekai_music_tags_api,
                                              get_sekai_musics_api)
from module.time_formatting import format_date_jp
from utility.modules import defaultEmbed


#music_info
async def get_music_info(music_id: int, session: aiohttp.ClientSession):
    music_api = await get_sekai_musics_api(session)
    for thing in music_api:
        if int(music_id) == thing['id']:
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
    
    def get_difficulty_level(difficulty):
        for thing in music_api:
            if thing['musicDifficulty'] == f'{difficulty}':
                level = thing['playLevel']
            else: level = None
            return level
                
    def get_difficulty_note_count(difficulty):
        for thing in music_api:
            if thing['musicDifficulty'] == f'{difficulty}':
                note_count = thing['noteCount']
            else: note_count = None
            return note_count
        
    for thing in music_api:
        if int(music_id) == thing['musicId']:
            easy_level = get_difficulty_level('easy')
            easy_note_count = get_difficulty_note_count('easy')
            normal_level = get_difficulty_level('normal')
            normal_note_count = get_difficulty_note_count('normal')
            hard_level = get_difficulty_level('hard')
            hard_note_count =get_difficulty_note_count('hard')
            expert_level = get_difficulty_level('expert')
            expert_note_count = get_difficulty_note_count('expert')
            master_level = get_difficulty_level('master')
            master_note_count = get_difficulty_note_count('master')
            
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
            music_id = str(music_id)

            info = await get_music_info(music_id, session)
            difficulty = await get_music_difficulty_info(music_id, session)

            if len(music_id) == 1:
                music_asset_name = f'jacket_s_00{music_id}'
            elif len(music_id) == 2:
                music_asset_name = f'jacket_s_0{music_id}'
            elif len(music_id) == 3:
                music_asset_name = f'jacket_s_{music_id}'

            cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
            music_url = f'https://sekai.best/music/{music_id}'

            embed = defaultEmbed(title=f'**{info[0]}**')
            embed.set_thumbnail(url=cover_url)
            embed.add_field(name='作詞', value = f'{info[1]}', inline=True)
            embed.add_field(name='作曲', value = f'{info[2]}', inline=True)
            embed.add_field(name='編曲', value = f'{info[3]} \n\u200b', inline=True)
            embed.add_field(name='發佈時間', value= f'{info[4]}', inline=False)
            embed.add_field(name='\u200b', value='**難度**', inline=False)
            embed.add_field(name=f'Easy',
                            value=f'等級：{difficulty[0]}\n音符數量：{difficulty[1]}', inline=True)
            embed.add_field(name=f'Normal',
                            value=f'等級：{difficulty[2]}\n音符數量：{difficulty[3]}', inline=True)
            embed.add_field(name=f'Hard',
                            value=f'等級：{difficulty[4]}\n音符數量：{difficulty[5]}', inline=True)
            embed.add_field(name=f'Expert',
                            value=f'等級：{difficulty[6]}\n音符數量：{difficulty[7]}', inline=True)
            embed.add_field(name=f'Master',
                            value=f'等級：{difficulty[8]}\n音符數量：{difficulty[9]}\n\u200b', inline=True)
            embed.add_field(name='\u200b', value='\u200b', inline=True)
            embed.add_field(name='更多資訊', value=music_url, inline=False) 
            
            group_music_embed_list.append(embed)
            
async def get_music_embed(music_id: str, session: aiohttp.ClientSession):
    
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
    embed.add_field(name='作詞', value = f'{info[1]}', inline=True)
    embed.add_field(name='作曲', value = f'{info[2]}', inline=True)
    embed.add_field(name='編曲', value = f'{info[3]} \n\u200b', inline=True)
    embed.add_field(name='發佈時間', value= f'{info[4]}', inline=False)
    embed.add_field(name='\u200b', value='**難度**', inline=False)
    embed.add_field(name=f'Easy',
                    value=f'等級：{difficulty[0]}\n音符數量：{difficulty[1]}', inline=True)
    embed.add_field(name=f'Normal',
                    value=f'等級：{difficulty[2]}\n音符數量：{difficulty[3]}', inline=True)
    embed.add_field(name=f'Hard',
                    value=f'等級：{difficulty[4]}\n音符數量：{difficulty[5]}', inline=True)
    embed.add_field(name=f'Expert',
                    value=f'等級：{difficulty[6]}\n音符數量：{difficulty[7]}', inline=True)
    embed.add_field(name=f'Master',
                    value=f'等級：{difficulty[8]}\n音符數量：{difficulty[9]}\n\u200b', inline=True)
    embed.add_field(name='\u200b', value='\u200b', inline=True)
    embed.add_field(name='更多資訊', value=music_url, inline=False) 
            
    return embed
