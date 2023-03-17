import time

from sekai.sekai_modules.main import get_data, get_resource_box


class EventInfo(object):
    def __init__(self):
        self.id = 0
        self.eventType = ''
        self.name = ''    
        self.assetbundleName = ''
        self.bgmAssetbundleName = ''
        self.eventPointAssetbundleName = ''
        self.startAt = 0
        self.aggregateAt = 0
        self.rankingAnnounceAt = 0
        self.closedAt = 0
        self.virtualLiveId = 0
        self.unit = 0
        self.eventRankingRewardRanges = []
        self.eventCharacters = []
        self.eventBonusAttribute = ''
        
    async def get_event_info(self, event_id: int, server: str):
        data = await get_data(server=f'{server}', type='diff', path='master/events.json')  
        data2 = await get_data(server=f'{server}', type='diff', path='master/eventDeckBonuses.json')    
        data3 = await get_data(server=f'tw', type='diff', path='main/gameCharacters.json')  
          
        for event in data:
            if event['id'] == event_id:
                self.id = event['id']
                self.eventType = event['eventType']
                self.name = event['name']
                self.assetbundleName = event['assetbundleName']
                self.bgmAssetbundleName = event['bgmAssetbundleName']
                self.eventPointAssetbundleName = event['eventPointAssetbundleName']
                self.startAt = event['startAt']
                self.aggregateAt = event['aggregateAt']
                self.rankingAnnounceAt = event['rankingAnnounceAt']
                self.closedAt = event['closedAt']
                self.virtualLiveId = event['virtualLiveId']
                self.unit = event['unit']
                self.eventRankingRewardRanges = event['eventRankingRewardRanges']
                for id in data2:
                    if self.id == id['eventId']:
                        character_id = id.get('gameCharacterUnitId')
                        self.eventBonusAttribute = id.get('cardAttr')
                        for character in data3:
                            if character_id == character['id']:
                                first_name = character['firstName']
                                last_name = character['givenName']
                                name = f'{first_name}{last_name}'
                                self.eventCharacters.append(name)
                if None in self.eventCharacters:
                    self.eventCharacters.remove(None)
                self.eventCharacters = list(dict.fromkeys(self.eventCharacters))
                
                
async def find_current_event_id(server: str):
    server = server
    data = await get_data(server=f'{server}', type='diff', path='master/events.json')         
    for event in data:
        event_start_time = event['startAt']
        event_end_time = event['aggregateAt']
        current_time = int(time.time())
        current_time *= 1000  
        if current_time >= event_start_time and current_time <= event_end_time:     
            return event['id']
    else:
        return None  
    
async def process_event_rewards(server: str, event_id: int):
    event_info = EventInfo()
    await event_info.get_event_info(event_id=event_id, server=server)
    event_rewards = event_info.eventRankingRewardRanges
    string = ''
    for range in event_rewards:
        if range['fromRank'] == range['toRank']:
            from_rank = range['fromRank']
            resource_box_id = range['eventRankingReward'][0]['resourceBoxId']
            items = await get_resource_box('event_ranking_reward', resource_box_id)
            text = f'第 {from_rank} 名\n'
            text += f'{items}\n'
        else:
            from_rank = range['fromRank']
            to_rank = range['toRank']
            resource_box_id = range['eventRankingReward'][0]['resourceBoxId']
            items = await get_resource_box('event_ranking_reward', resource_box_id)
            text = f'第 {from_rank} 名至第 {to_rank} 名\n'
            text += f'{items}\n'
        string += text
        
    return string
        