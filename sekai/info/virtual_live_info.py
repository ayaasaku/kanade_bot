from sekai.sekai_modules.main import get_data


class VirtualLiveInfo(object):
    def __init__(self):
        self.id = 0
        self.virtualLiveType = ''
        self.virtualLivePlatform = ''
        self.seq = 0
        self.name = ''
        self.assetbundleName = ''
        self.screenMvMusicVocalId = 0
        self.startAt = 0
        self.endAt = 0
        self.rankingAnnounceAt = 0
        self.virtualLiveSetList = []
        self.virtualLiveBeginnerSchdules = []
        self.virtualLiveSchedules = []
        self.virtualLiveCharacters = []
        self.virtualLiveRewards = []
        self.virtualLiveWaitingRoom = {}
        self.virtualItems = []
        self.virtualLiveAppeals = []
        self.virtualLiveInformation = {}
        
    async def get_virtual_live_info(self, music_id: int, server: str):
        data = await get_data(server=f'{server}', type='diff', path='main/virtualLives.json')  
    
        for music in data:
            if music['id'] == music_id:
                self.id = music['id']
                try: self.seq = music['seq']
                except: pass
                self.releaseConditionId = music['releaseConditionId']
                self.categories = music['categories']
                self.title = music['title']
                try: self.pronunciation = music['pronunciation']
                except: pass
                self.lyricist = music['lyricist']
                self.composer = music['composer']
                self.arranger = music['arranger']
                self.dancerCount = music['dancerCount']
                self.selfDancerPosition = music['selfDancerPosition']
                self.assetbundleName = music['assetbundleName']
                self.publishedAt = music['publishedAt']
                self.fillerSec = music['fillerSec']
                try: self.liveTalkBackgroundAssetbundleName = music['liveTalkBackgroundAssetbundleName']
                except: pass
                try: self.liveStageId = music['liveStageId']
                except: pass
                try: self.infos = music['infos']
                except: pass
                break
            