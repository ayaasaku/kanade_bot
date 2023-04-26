from sekai.sekai_modules.main import get_data


class MusicInfo(object):
    def __init__(self):
        self.id = 0
        self.seq = 0
        self.releaseConditionId = 0
        self.categories = []   
        self.title = ''
        self.pronunciation = ''
        self.lyricist = ''
        self.composer = ''
        self.arranger = ''
        self.dancerCount = 0
        self.selfDancerPosition = 0
        self.assetbundleName = ''
        self.liveTalkBackgroundAssetbundleName = ''
        self.publishedAt = 0
        self.liveStageId = 0
        self.fillerSec = 0
        self.infos = []
        self.difficulties = []
        
    async def get_music_info(self, music_id: int, server: str):
        data = await get_data(server=f'{server}', type='diff', path='main/musics.json')  
        data2 = await get_data(server=f'{server}', type='diff', path='main/musicDifficulties.json')
    
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
            
        for difficulty in data2:
            if difficulty['musicId'] == music_id:
                small_dict = {
                    'id': difficulty['id'],
                    'musicId': difficulty['musicId'],
                    'musicDifficulty': difficulty['musicDifficulty'],
                    'playLevel': difficulty['playLevel'],
                    'releaseConditionId': difficulty['releaseConditionId'],
                    'noteCount': 999
                }
                try: small_dict['noteCount'] = difficulty['noteCount']
                except: small_dict['noteCount'] = difficulty['totalNoteCount']
                self.difficulties.append(small_dict)