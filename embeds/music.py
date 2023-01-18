import aiohttp
from modules.main import defaultEmbed
from sekai.info.music_info import MusicInfo
from sekai.sekai_modules.main import get_data, format_date

async def music_embed(server: str, group: str, session: aiohttp.ClientSession):
    diff = await get_data(server=server, type='diff', path='main/musicTags.json', session=session)
    group_music_embed_list = []
    for thing in diff:
        if thing['musicTag'] == f'{group}':
            music_id = thing['musicId']

            music_info = MusicInfo()
            await music_info.get_music_info(music_id=music_id, server=server, session=session)
            
            asset_name = music_info.assetbundleName

            album_cover_url = f"https://minio.dnaroma.eu/sekai-assets/music/jacket/{asset_name}_rip/{asset_name}.webp"
            music_url = f'https://sekai.best/music/{music_id}'

            release_date = format_date(server=server, seconds=music_info.publishedAt // 1000)
            try: embed = defaultEmbed(title=f'**{music_info.title}**', description=f'{music_info.pronunciation} \n\u200b')
            except: embed = defaultEmbed(title=f'**{music_info.title}**')
            embed.set_thumbnail(url=album_cover_url)
            embed.add_field(name='作詞', value = f'{music_info.lyricist}', inline=True)
            embed.add_field(name='作曲', value = f'{music_info.composer}', inline=True)
            embed.add_field(name='編曲', value = f'{music_info.arranger}', inline=True)
            embed.add_field(name='\u200b', value='**難度**', inline=False)

            for difficulty in music_info.difficulties:
                name = difficulty['musicDifficulty']
                level = difficulty['playLevel']
                note_count = difficulty['noteCount']
                embed.add_field(name=f'{name.capitalize()}',
                            value=f'等級：{level}\n音符數量：{note_count}', inline=True)
                
            embed.add_field(name='\u200b', value='\u200b', inline=True)   
            embed.add_field(name='\u200b\n 發佈時間', value= f'{release_date}', inline=False) 
            embed.add_field(name='更多資訊', value=music_url, inline=False) 
            group_music_embed_list.append(embed)
            
    return group_music_embed_list
