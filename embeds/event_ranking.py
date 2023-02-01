import time

from modules.main import defaultEmbed, errEmbed

from sekai.sekai_modules.main import get_data, format_date, format_time, format_progress, format_hour
from sekai.info.event_info import EventInfo, find_current_event_id
from sekai.user.event_ranking.event_ranking import UserEventRanking

async def event_ranking_embed(server: str, user_id: str):
    event_ranking_info = UserEventRanking()
    event_info = EventInfo()
    current_event_id = await find_current_event_id(server=server)
    
    if current_event_id == None:
        embed = errEmbed('現時並沒有舉行任何活動')
    else:
        await event_info.get_event_info(event_id=current_event_id, server=server)       
        event_name = event_info.name
        event_banner_name = event_info.assetbundleName
        logo_url = await get_data(server=server, type='assets', path=f'event/{event_banner_name}/logo_rip/logo.webp')
        banner_url = await get_data(server=server, type='assets', path=f'home/banner/{event_banner_name}_rip/{event_banner_name}.webp')
        current_time = int(time.time())   
        event_start_time = event_info.startAt // 1000
        seconds_passed = current_time - event_start_time
        hours_passed = format_hour(seconds_passed)
        
        await event_ranking_info.get_user_event_ranking(event_id=current_event_id, server=server, user_id=user_id)
        name = event_ranking_info.name
        rank = event_ranking_info.rank
        score = event_ranking_info.score
        score_per_hour = score // hours_passed
        
        '''ranking_reward_range = event_info.eventRankingRewardRanges
        for thing in ranking_reward_range:
            start = thing['fromRank']
            end = thing['toRank']
            if rank in range(start, end):
                resource_box_id = thing['eventRankingRewards'][0]['resourceBoxId']
                break'''
            
        embed = defaultEmbed(title=f'**活動排名**', description=f'**{event_name}**')
        embed.set_thumbnail(url=logo_url)
        embed.set_image(url=banner_url)
        embed.add_field(name=f'玩家名稱', value=f'{name}', inline=True)
        embed.add_field(name=f'排名', value=f'No.{rank}', inline=True)
        embed.add_field(name=f'點數', value=f'{score}P', inline=True)
        embed.add_field(name='平均時速', value=f'{score_per_hour}P', inline=False)
        
    return embed