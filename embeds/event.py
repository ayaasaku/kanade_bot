import time

from modules.main import defaultEmbed, errEmbed

from sekai.sekai_modules.main import get_data, format_date, format_time, format_progress
from sekai.info.event_info import EventInfo, find_current_event_id, process_event_rewards

from data.emoji_data import attributes
from data.translate_data import translate


async def timeleft_embed(server: str):
    event_info = EventInfo()
    current_event_id = await find_current_event_id(server=server)
    
    if current_event_id == None:
        embed = errEmbed('現時並沒有舉行任何活動')
    else:
        await event_info.get_event_info(event_id=current_event_id, server=server)       
        current_time = int(time.time())   
        event_id = event_info.id
        event_end_time = event_info.aggregateAt // 1000
        event_name = event_info.name
        event_start_time = event_info.startAt // 1000
        event_banner_name = event_info.assetbundleName
        event_end_date = format_date(server=server, seconds = event_end_time)
        logo_url = await get_data(server=server, type='assets', path=f'event/{event_banner_name}/logo_rip/logo.webp')
        banner_url = await get_data(server=server, type='assets', path=f'home/banner/{event_banner_name}_rip/{event_banner_name}.webp')
        event_url = f'https://sekai.best/event/{event_id}'
        time_left = format_time(event_end_time - current_time)
        event_progress = format_progress(event_end_time, event_start_time, current_time)
        
        embed = defaultEmbed(title=f'**{event_name}**')
        embed.set_thumbnail(url=logo_url)
        embed.set_image(url=banner_url)
        embed.add_field(name=f'剩餘時間', value=f'{time_left}', inline=False)
        embed.add_field(name=f'進度', value=f'{event_progress}', inline=False)
        embed.add_field(name=f'結束日期', value=f'{event_end_date}', inline=False)
        embed.add_field(name='更多資訊', value=event_url, inline=False)
        
    return embed
               
               
async def event_embed(server: str):     
    event_info = EventInfo()
    current_event_id = await find_current_event_id(server=server)
    
    if current_event_id == None:
        embed = errEmbed('現時並沒有舉行任何活動')
    else:
        await event_info.get_event_info(event_id=current_event_id, server=server)       
        event_id = event_info.id
        event_end_time = event_info.aggregateAt
        event_name = event_info.name
        event_start_time = event_info.startAt
        event_banner_name = event_info.assetbundleName
        event_bonus_attribute = event_info.eventBonusAttribute
        event_type = event_info.eventType
        event_bonus_characters_name_list = event_info.eventCharacters
        event_start_date = format_date(server=server, seconds = event_start_time // 1000)
        event_end_date = format_date(server=server, seconds = event_end_time // 1000)
        logo_url = await get_data(server=server, type='assets', path=f'event/{event_banner_name}/logo_rip/logo.webp')
        error_logo_url = f'https://static.vecteezy.com/system/resources/previews/005/337/799/original/icon-image-not-found-free-vector.jpg'
        banner_url = await get_data(server=server, type='assets', path=f'home/banner/{event_banner_name}_rip/{event_banner_name}.webp')
        error_banner_url = f'https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png'
        event_url = f'https://sekai.best/event/{event_id}'
        attribute_emoji = attributes[event_bonus_attribute]
        event_attribute_translated = translate['attributes'][event_bonus_attribute]
        event_type_translated = translate['event_type'][event_type]
        event_bonus_attribute = event_bonus_attribute.capitalize()
        event_rewards = await process_event_rewards(server=server, event_id=event_id)
        
        embed = defaultEmbed(title=f'**{event_name}**')
        try: embed.set_thumbnail(url=logo_url)
        except: embed.set_thumbnail(url=error_logo_url)
        try: embed.set_image(url=banner_url)
        except: embed.set_image(url=error_banner_url)
        embed.add_field(name='活動類型', value=event_type_translated, inline=False)  
        embed.add_field(name='加成屬性', value=f'{attribute_emoji} {event_bonus_attribute}\n({event_attribute_translated})', inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        
        if len(event_bonus_characters_name_list) == 1:
            embed.add_field(name='加成角色', value=f'{event_bonus_characters_name_list[0]}', inline=True)  
        elif len(event_bonus_characters_name_list) == 2:
            embed.add_field(name='加成角色', value=f'{event_bonus_characters_name_list[0]}，{event_bonus_characters_name_list[1]}', inline=True)      
        elif len(event_bonus_characters_name_list) == 3:
            embed.add_field(name='加成角色', value=f'{event_bonus_characters_name_list[0]}，{event_bonus_characters_name_list[1]}\n{event_bonus_characters_name_list[2]}', inline=True)      
        elif len(event_bonus_characters_name_list) == 4:
            embed.add_field(name='加成角色', value=f'{event_bonus_characters_name_list[0]}，{event_bonus_characters_name_list[1]}\n{event_bonus_characters_name_list[2]}，{event_bonus_characters_name_list[3]}', inline=True)  
        elif len(event_bonus_characters_name_list) == 5:
            embed.add_field(name='加成角色', value=f'{event_bonus_characters_name_list[0]}，{event_bonus_characters_name_list[1]}\n{event_bonus_characters_name_list[2]}，{event_bonus_characters_name_list[3]}\n{event_bonus_characters_name_list[4]}', inline=True)  
        embed.add_field(name='開始', value=event_start_date, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='結束', value=f'{event_end_date}', inline=True)
        embed.add_field(name='活動排名獎勵', value=event_rewards, inline=False)
        embed.add_field(name='更多資訊', value=event_url, inline=False)
        
    return embed