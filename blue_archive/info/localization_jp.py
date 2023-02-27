import time, aiohttp

from modules.main import get_data

class LocalizationInfoJp(object):
    def __init__(self):
        self.SquadType = {}
        self.BulletType = {}
        self.ArmorType = {}
        self.ArmorTypeLong = {}
        self.TacticRole = {}
        self.School = {}
        self.AdaptionType = {}
        self.SchoolLong = {}
        self.Club = {}
        self.BossFaction = {}
        self.Stat = {}
        self.IsLimited = {}
        self.FurnitureSet = {}
        self.ItemCategory = {}
        self.ArtifactClass = {}
        self.EnemyTags = {}
        self.EventName = {}
        self.StageType = {}
        self.TimeAttackStage = {}
        self.ConquestMap = {}
        self.StageTitle = {}
        self.EnemyRank = {}
        self.NodeQuality = {}
        self.NodeTier = {}
        self.RaidDifficulty = {}
        self.WeaponPartExpBonus = {}
        self.BuffType = {}
        self.BuffName = {}
        self.BuffNameLong = {}
        self.BuffTooltip = {}
        self.ServerName = {}
        self.ShopCategory = {}
        self.GroggyCondition = {}
        self.ui = {}
       
        
        
    async def get_localization_jp(self):
        data = get_data('https://lonqie.github.io/SchaleDB/data/jp/localization.json' 'text/plain')
        self.School = data['School']
        self.Club = data['Club']
        
            
                
                

        
        
 