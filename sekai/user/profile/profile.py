import aiohttp
from sekai.sekai_modules.main import get_data
class UserProfile(object):
    def __init__(self):
        #user['userGamedata']
        self.userId = 0
        self.name = ''
        self.deck = 0
        self.rank = 0
        #userProfile
        self.word = ''
        self.twitterId = ''
        self.profileImageType = ''
        #userDecks
        self.userDecks = {}
        #userCards
        self.userCards = []
        #userMusics
        self.userMusics = []
        #userCharacters
        self.userCharacters = []
        #userChallengeLiveSoloResults
        self.userChallengeLiveSoloResults = []
        #userChallengeLiveSoloStages
        self.userChallengeLiveSoloStages = []
        #userAreaItems
        self.userAreaItems = []
        #userHonors
        self.userHonors = []
        #userBondsHonors
        self.userBondsHonors = []
        #userMusicResults
        self.userMusicResults = []
        #userCustomProfileCards
        self.userCustomProfileCards = []
        #userProfileHonors
        self.userProfileHonors = []

    async def get_profile(self, user_id: str, session: aiohttp.ClientSession):    
        data = await get_data(server='jp', type='api', path=f'/user/{user_id}/profile', session=session)
        self.userId = data['user']['userGamedata']['userId']
        if int(user_id) != self.userId: raise SystemError('API error')
        self.name = data['user']['userGamedata']['name']
        self.deck = data['user']['userGamedata']['deck']
        self.rank = data['user']['userGamedata']['rank']
        try: self.word = data['userProfile']['word']
        except: self.word = None
        try: self.twitterId = data['userProfile']['twitterId']
        except: self.twitterId = None
        self.profileImageType = data['userProfile']['profileImageType']
        self.userDecks = data['userDecks'][0]
        self.userCards = data['userCards']
        self.userMusics = data['userMusics']
        self.userCharacters = data['userCharacters']
        self.userChallengeLiveSoloResults = data['userChallengeLiveSoloResults']
        self.userChallengeLiveSoloStages = data['userChallengeLiveSoloStages']
        self.userAreaItems = data['userAreaItems']
        self.userHonors = data['userHonors']
        self.userBondsHonors = data['userBondsHonors']
        self.userMusicResults = data['userMusicResults']
        self.userCustomProfileCards = data['userCustomProfileCards']
        self.userProfileHonors = data['userProfileHonors']
        
