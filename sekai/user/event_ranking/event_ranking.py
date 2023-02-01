from sekai.sekai_modules.main import get_data

class UserEventRanking(object):
    def __init__(self):
        self.isOwn = False
        self.name  = ''
        self.rank = 0
        self.score = 0
        self.userCard = {}

    async def get_user_event_ranking(self, event_id, server: str, user_id: str):    
        data = await get_data(server='jp', type='api', path=f'event/{event_id}/user/{server}/{user_id}/')
        data = data['rankings'][0]
        self.isOwn = data['isOwn']
        self.name = data['name']
        self.rank = data['rank']
        self.score = data['score']
        self.userCard = data['userCard']
        
        
