import aiohttp
from utility.apps.sekai.api_functions import (get_sekai_music_difficulties_api,
                                              get_sekai_music_tags_api,
                                              get_sekai_musics_api)
from utility.utils import defaultEmbed
from utility.apps.sekai.time_formatting import format_date_jp

async def get_vocaloid_music(session: aiohttp.ClientSession):
    group_music_embed_list = []
    tag_api = await get_sekai_music_tags_api(session)
    info_api = await get_sekai_musics_api(session)
    difficulty_api = await get_sekai_music_difficulties_api(session)
    for tag in tag_api:
        if tag['musicTag'] == 'vocaloid':
            music_id = tag['musicId']
    
        for info in info_api:
            if music_id == info['id']:
                title = info['title']
                lyricist = info['lyricist']
                composer = info['composer']
                arranger = info['arranger']
                published_time = await format_date_jp(info['publishedAt'])

        for thing in difficulty_api:
            if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
                easy_level = thing['playLevel']
                easy_note_count = thing['noteCount']
            
            elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'normal':    
                normal_level = thing['playLevel']
                normal_note_count = thing['noteCount']
                
            elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'hard':        
                hard_level = thing['playLevel']
                hard_note_count = thing['noteCount']
            
            elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'expert':       
                expert_level = thing['playLevel']
                expert_note_count = thing['noteCount']
            
            elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'master':        
                master_level = thing['playLevel']
                master_note_count = thing['noteCount']
                
                if len(str(music_id)) == 1:
                    music_asset_name = f'jacket_s_00{music_id}'
                elif len(str(music_id)) == 2:
                    music_asset_name = f'jacket_s_0{music_id}'
                elif len(str(music_id)) == 3:
                    music_asset_name = f'jacket_s_{music_id}'

                cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
                music_url = f'https://sekai.best/music/{music_id}'

                embed = defaultEmbed(title=f'**{title}**')
                embed.set_thumbnail(url=cover_url)
                embed.add_field(name='作詞', value=lyricist, inline=True)
                embed.add_field(name='作曲', value=composer, inline=True)
                embed.add_field(name='編曲', value=f'{arranger}\n\u200b', inline=True)
                embed.add_field(name='發佈時間', value=published_time, inline=False)
                embed.add_field(name='\u200b', value='**難度**', inline=False)
                embed.add_field(name='Easy',
                                value=f'等級：{easy_level}\n音符數量：{easy_note_count}', inline=True)
                embed.add_field(name='Normal',
                                value=f'等級：{normal_level}\n音符數量：{normal_note_count}', inline=True)
                embed.add_field(name='Hard',
                                value=f'等級：{hard_level}\n音符數量：{hard_note_count}', inline=True)
                embed.add_field(name='Expert',
                                value=f'等級：{expert_level}\n音符數量：{expert_note_count}', inline=True)
                embed.add_field(name='Master',
                                value=f'等級：{master_level}\n音符數量：{master_note_count}\n\u200b', inline=True)
                embed.add_field(name='\u200b', value='\u200b', inline=True)
                embed.add_field(name='更多資訊', value=music_url, inline=False)
                
                
                group_music_embed_list.append(embed)
            
    return group_music_embed_list

async def get_school_refusal_music(session: aiohttp.ClientSession):
    group_music_embed_list = []
    tag_api = await get_sekai_music_tags_api(session)
    info_api = await get_sekai_musics_api(session)
    difficulty_api = await get_sekai_music_difficulties_api(session)
    for tag in tag_api:
        if tag['musicTag'] == 'school_refusal':
            music_id = tag['musicId']
    
            for info in info_api:
                if music_id == info['id']:
                    title = info['title']
                    lyricist = info['lyricist']
                    composer = info['composer']
                    arranger = info['arranger']
                    published_time = await format_date_jp(info['publishedAt'])

            for thing in difficulty_api:
                if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
                    easy_level = thing['playLevel']
                    easy_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'normal':    
                    normal_level = thing['playLevel']
                    normal_note_count = thing['noteCount']
                    
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'hard':        
                    hard_level = thing['playLevel']
                    hard_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'expert':       
                    expert_level = thing['playLevel']
                    expert_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'master':        
                    master_level = thing['playLevel']
                    master_note_count = thing['noteCount']
                    
                    if len(str(music_id)) == 1:
                        music_asset_name = f'jacket_s_00{music_id}'
                    elif len(str(music_id)) == 2:
                        music_asset_name = f'jacket_s_0{music_id}'
                    elif len(str(music_id)) == 3:
                        music_asset_name = f'jacket_s_{music_id}'

                    cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
                    music_url = f'https://sekai.best/music/{music_id}'

                    embed = defaultEmbed(title=f'**{title}**')
                    embed.set_thumbnail(url=cover_url)
                    embed.add_field(name='作詞', value=lyricist, inline=True)
                    embed.add_field(name='作曲', value=composer, inline=True)
                    embed.add_field(name='編曲', value=f'{arranger}\n\u200b', inline=True)
                    embed.add_field(name='發佈時間', value=published_time, inline=False)
                    embed.add_field(name='\u200b', value='**難度**', inline=False)
                    embed.add_field(name='Easy',
                                    value=f'等級：{easy_level}\n音符數量：{easy_note_count}', inline=True)
                    embed.add_field(name='Normal',
                                    value=f'等級：{normal_level}\n音符數量：{normal_note_count}', inline=True)
                    embed.add_field(name='Hard',
                                    value=f'等級：{hard_level}\n音符數量：{hard_note_count}', inline=True)
                    embed.add_field(name='Expert',
                                    value=f'等級：{expert_level}\n音符數量：{expert_note_count}', inline=True)
                    embed.add_field(name='Master',
                                    value=f'等級：{master_level}\n音符數量：{master_note_count}\n\u200b', inline=True)
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                    embed.add_field(name='更多資訊', value=music_url, inline=False) 
                    
                    group_music_embed_list.append(embed)
            
    return group_music_embed_list

async def get_light_music_club_music(session: aiohttp.ClientSession):
    group_music_embed_list = []
    tag_api = await get_sekai_music_tags_api(session)
    info_api = await get_sekai_musics_api(session)
    difficulty_api = await get_sekai_music_difficulties_api(session)
    for tag in tag_api:
        if tag['musicTag'] == 'light_music_club':
            music_id = tag['musicId']
    
            for info in info_api:
                if music_id == info['id']:
                    title = info['title']
                    lyricist = info['lyricist']
                    composer = info['composer']
                    arranger = info['arranger']
                    published_time = await format_date_jp(info['publishedAt'])

            for thing in difficulty_api:
                if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
                    easy_level = thing['playLevel']
                    easy_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'normal':    
                    normal_level = thing['playLevel']
                    normal_note_count = thing['noteCount']
                    
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'hard':        
                    hard_level = thing['playLevel']
                    hard_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'expert':       
                    expert_level = thing['playLevel']
                    expert_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'master':        
                    master_level = thing['playLevel']
                    master_note_count = thing['noteCount']
                    
                    if len(str(music_id)) == 1:
                        music_asset_name = f'jacket_s_00{music_id}'
                    elif len(str(music_id)) == 2:
                        music_asset_name = f'jacket_s_0{music_id}'
                    elif len(str(music_id)) == 3:
                        music_asset_name = f'jacket_s_{music_id}'

                    cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
                    music_url = f'https://sekai.best/music/{music_id}'

                    embed = defaultEmbed(title=f'**{title}**')
                    embed.set_thumbnail(url=cover_url)
                    embed.add_field(name='作詞', value=lyricist, inline=True)
                    embed.add_field(name='作曲', value=composer, inline=True)
                    embed.add_field(name='編曲', value=f'{arranger}\n\u200b', inline=True)
                    embed.add_field(name='發佈時間', value=published_time, inline=False)
                    embed.add_field(name='\u200b', value='**難度**', inline=False)
                    embed.add_field(name='Easy',
                                    value=f'等級：{easy_level}\n音符數量：{easy_note_count}', inline=True)
                    embed.add_field(name='Normal',
                                    value=f'等級：{normal_level}\n音符數量：{normal_note_count}', inline=True)
                    embed.add_field(name='Hard',
                                    value=f'等級：{hard_level}\n音符數量：{hard_note_count}', inline=True)
                    embed.add_field(name='Expert',
                                    value=f'等級：{expert_level}\n音符數量：{expert_note_count}', inline=True)
                    embed.add_field(name='Master',
                                    value=f'等級：{master_level}\n音符數量：{master_note_count}\n\u200b', inline=True)
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                    embed.add_field(name='更多資訊', value=music_url, inline=False)
                    
                    group_music_embed_list.append(embed)
                
        return group_music_embed_list

async def get_idol_music(session: aiohttp.ClientSession):
    group_music_embed_list = []
    tag_api = await get_sekai_music_tags_api(session)
    info_api = await get_sekai_musics_api(session)
    difficulty_api = await get_sekai_music_difficulties_api(session)
    
    for tag in tag_api:
        if tag['musicTag'] == 'idol':
            music_id = tag['musicId']
    
            for info in info_api:
                if music_id == info['id']:
                    title = info['title']
                    lyricist = info['lyricist']
                    composer = info['composer']
                    arranger = info['arranger']
                    published_time = await format_date_jp(info['publishedAt'])

            for thing in difficulty_api:
                if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
                    easy_level = thing['playLevel']
                    easy_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'normal':    
                    normal_level = thing['playLevel']
                    normal_note_count = thing['noteCount']
                    
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'hard':        
                    hard_level = thing['playLevel']
                    hard_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'expert':       
                    expert_level = thing['playLevel']
                    expert_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'master':        
                    master_level = thing['playLevel']
                    master_note_count = thing['noteCount']
                    
                    if len(str(music_id)) == 1:
                        music_asset_name = f'jacket_s_00{music_id}'
                    elif len(str(music_id)) == 2:
                        music_asset_name = f'jacket_s_0{music_id}'
                    elif len(str(music_id)) == 3:
                        music_asset_name = f'jacket_s_{music_id}'

                    cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
                    music_url = f'https://sekai.best/music/{music_id}'

                    embed = defaultEmbed(title=f'**{title}**')
                    embed.set_thumbnail(url=cover_url)
                    embed.add_field(name='作詞', value=lyricist, inline=True)
                    embed.add_field(name='作曲', value=composer, inline=True)
                    embed.add_field(name='編曲', value=f'{arranger}\n\u200b', inline=True)
                    embed.add_field(name='發佈時間', value=published_time, inline=False)
                    embed.add_field(name='\u200b', value='**難度**', inline=False)
                    embed.add_field(name='Easy',
                                    value=f'等級：{easy_level}\n音符數量：{easy_note_count}', inline=True)
                    embed.add_field(name='Normal',
                                    value=f'等級：{normal_level}\n音符數量：{normal_note_count}', inline=True)
                    embed.add_field(name='Hard',
                                    value=f'等級：{hard_level}\n音符數量：{hard_note_count}', inline=True)
                    embed.add_field(name='Expert',
                                    value=f'等級：{expert_level}\n音符數量：{expert_note_count}', inline=True)
                    embed.add_field(name='Master',
                                    value=f'等級：{master_level}\n音符數量：{master_note_count}\n\u200b', inline=True)
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                    embed.add_field(name='更多資訊', value=music_url, inline=False)
                    
                    group_music_embed_list.append(embed)
                
    return group_music_embed_list

async def get_street_music(session: aiohttp.ClientSession):
    group_music_embed_list = []
    
    tag_api = await get_sekai_music_tags_api(session)
    info_api = await get_sekai_musics_api(session)
    difficulty_api = await get_sekai_music_difficulties_api(session)
    
    for tag in tag_api:
        if tag['musicTag'] == 'street':
            music_id = tag['musicId']
    
            for info in info_api:
                if music_id == info['id']:
                    title = info['title']
                    lyricist = info['lyricist']
                    composer = info['composer']
                    arranger = info['arranger']
                    published_time = await format_date_jp(info['publishedAt'])

            for thing in difficulty_api:
                if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
                    easy_level = thing['playLevel']
                    easy_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'normal':    
                    normal_level = thing['playLevel']
                    normal_note_count = thing['noteCount']
                    
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'hard':        
                    hard_level = thing['playLevel']
                    hard_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'expert':       
                    expert_level = thing['playLevel']
                    expert_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'master':        
                    master_level = thing['playLevel']
                    master_note_count = thing['noteCount']
                    
                    if len(str(music_id)) == 1:
                        music_asset_name = f'jacket_s_00{music_id}'
                    elif len(str(music_id)) == 2:
                        music_asset_name = f'jacket_s_0{music_id}'
                    elif len(str(music_id)) == 3:
                        music_asset_name = f'jacket_s_{music_id}'

                    cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
                    music_url = f'https://sekai.best/music/{music_id}'

                    embed = defaultEmbed(title=f'**{title}**')
                    embed.set_thumbnail(url=cover_url)
                    embed.add_field(name='作詞', value=lyricist, inline=True)
                    embed.add_field(name='作曲', value=composer, inline=True)
                    embed.add_field(name='編曲', value=f'{arranger}\n\u200b', inline=True)
                    embed.add_field(name='發佈時間', value=published_time, inline=False)
                    embed.add_field(name='\u200b', value='**難度**', inline=False)
                    embed.add_field(name='Easy',
                                    value=f'等級：{easy_level}\n音符數量：{easy_note_count}', inline=True)
                    embed.add_field(name='Normal',
                                    value=f'等級：{normal_level}\n音符數量：{normal_note_count}', inline=True)
                    embed.add_field(name='Hard',
                                    value=f'等級：{hard_level}\n音符數量：{hard_note_count}', inline=True)
                    embed.add_field(name='Expert',
                                    value=f'等級：{expert_level}\n音符數量：{expert_note_count}', inline=True)
                    embed.add_field(name='Master',
                                    value=f'等級：{master_level}\n音符數量：{master_note_count}\n\u200b', inline=True)
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                    embed.add_field(name='更多資訊', value=music_url, inline=False)
                    
                    group_music_embed_list.append(embed)
                    
    return group_music_embed_list

async def get_theme_park_music(session: aiohttp.ClientSession):
    group_music_embed_list = []
    
    tag_api = await get_sekai_music_tags_api(session)
    info_api = await get_sekai_musics_api(session)
    difficulty_api = await get_sekai_music_difficulties_api(session)
    
    for tag in tag_api:
        if tag['musicTag'] == 'theme_park':
            music_id = tag['musicId']
    
            for info in info_api:
                if music_id == info['id']:
                    title = info['title']
                    lyricist = info['lyricist']
                    composer = info['composer']
                    arranger = info['arranger']
                    published_time = await format_date_jp(info['publishedAt'])

            for thing in difficulty_api:
                if music_id == thing['musicId'] and thing['musicDifficulty'] == 'easy':
                    easy_level = thing['playLevel']
                    easy_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'normal':    
                    normal_level = thing['playLevel']
                    normal_note_count = thing['noteCount']
                    
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'hard':        
                    hard_level = thing['playLevel']
                    hard_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'expert':       
                    expert_level = thing['playLevel']
                    expert_note_count = thing['noteCount']
                
                elif music_id == thing['musicId'] and thing['musicDifficulty'] == 'master':        
                    master_level = thing['playLevel']
                    master_note_count = thing['noteCount']
                    
                    if len(str(music_id)) == 1:
                        music_asset_name = f'jacket_s_00{music_id}'
                    elif len(str(music_id)) == 2:
                        music_asset_name = f'jacket_s_0{music_id}'
                    elif len(str(music_id)) == 3:
                        music_asset_name = f'jacket_s_{music_id}'

                    cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{music_asset_name}_rip/{music_asset_name}.webp"
                    music_url = f'https://sekai.best/music/{music_id}'

                    embed = defaultEmbed(title=f'**{title}**')
                    embed.set_thumbnail(url=cover_url)
                    embed.add_field(name='作詞', value=lyricist, inline=True)
                    embed.add_field(name='作曲', value=composer, inline=True)
                    embed.add_field(name='編曲', value=f'{arranger}\n\u200b', inline=True)
                    embed.add_field(name='發佈時間', value=published_time, inline=False)
                    embed.add_field(name='\u200b', value='**難度**', inline=False)
                    embed.add_field(name='Easy',
                                    value=f'等級：{easy_level}\n音符數量：{easy_note_count}', inline=True)
                    embed.add_field(name='Normal',
                                    value=f'等級：{normal_level}\n音符數量：{normal_note_count}', inline=True)
                    embed.add_field(name='Hard',
                                    value=f'等級：{hard_level}\n音符數量：{hard_note_count}', inline=True)
                    embed.add_field(name='Expert',
                                    value=f'等級：{expert_level}\n音符數量：{expert_note_count}', inline=True)
                    embed.add_field(name='Master',
                                    value=f'等級：{master_level}\n音符數量：{master_note_count}\n\u200b', inline=True)
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                    embed.add_field(name='更多資訊', value=music_url, inline=False)
                    
                    group_music_embed_list.append(embed)
            
    return group_music_embed_list