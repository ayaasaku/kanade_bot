from modules.main import get_data

class StudentInfo(object):
    def __init__(self):
        #student
        self.Id = 0
        self.IsReleased = []
        self.DefaultOrder = 0
        self.PathName = ''
        self.DevName = ''
        self.Name = ''
        self.School = ''
        self.Club = ''
        self.StarGrade = 0
        self.SquadType = ''
        self.TacticRole = ''
        self.Summons = []
        self.Position = ''
        self.BulletType = ''
        self.ArmorType = ''
        self.StreetBattleAdaptation = 0
        self.OutdoorBattleAdaptation = 0
        self.IndoorBattleAdaptation = 0
        self.WeaponType = ''
        self.WeaponImg = ''
        self.Cover = True
        self.Equipment = [],
        self.CollectionBG = ''
        self.CollectionTexture = ''
        self.FamilyName = ''
        self.FamilyNameRuby = ''
        self.PersonalName = ''
        self.SchoolYear = ''
        self.CharacterAge = ''
        self.Birthday = ''
        self.CharacterSSRNew = ''
        self.ProfileIntroduction = ''
        self.Hobby = ''
        self.CharacterVoice = ''
        self.BirthDay = ''
        self.ArtistName = ''
        self.CharHeightMetric = ''
        self.CharHeightImperial = ''
        self.StabilityPoint = 0
        self.AttackPower1 = 0
        self.AttackPower100 = 0
        self.MaxHP1 = 0
        self.MaxHP100 = 0
        self.DefensePower1 = 0
        self.DefensePower100 = 0
        self.HealPower1 = 0
        self.HealPower100 = 0
        self.DodgePoint = 0
        self.AccuracyPoint = 0
        self.CriticalPoint = 0
        self.CriticalDamageRate = 0
        self.AmmoCount = 0
        self.AmmoCost = 0
        self.Range = 0
        self.RegenCost = 0
        self.Skills = []
        self.FavorStatType = []
        self.FavorStatValue = []
        self.FavorAlts = []
        self.MemoryLobby = []
        self.MemoryLobbyBGM = ''
        self.FurnitureInteraction = []
        self.FavorItemUniqueTags = []
        self.IsLimited = 0
        self.Weapon = {}
        self.Gear = {}
        self.SkillExMaterial = []
        self.SkillExMaterialAmount = []
        self.SkillMaterial = []
        self.SkillMaterialAmount = []    
        
    async def get_student_info(self, character_id: int):
        data = get_data('https://lonqie.github.io/SchaleDB/data/tw/students.json', 'text/plain')
        
        for character in data:
            if character['id'] == character_id:
                self.Name = character['Name']
                self.StabilityPoint = str(character["StabilityPoint"])
                self.AttackPower1 = str(character["AttackPower1"])
                self.AttackPower100 = str(character["AttackPower100"])
                self.MaxHP1 = str(character["MaxHP1"])
                self.MaxHP100 = str(character["MaxHP100"])
                self.DefensePower1 = str(character["DefensePower1"])
                self.DefensePower100 = str(character["DefensePower100"])
                self.HealPower1 = str(character["HealPower1"])
                self.HealPower100 = str(character["HealPower100"])
                self.DodgePoint = str(character["DodgePoint"])
                self.AccuracyPoint = str(character["AccuracyPoint"])
                self.CriticalPoint = str(character["CriticalPoint"])
                self.CriticalDamageRate = str(int(character["CriticalDamageRate"]/100))+"%"
                self.AmmoCount = str(character["AmmoCount"])
                self.AmmoCost = str(character["AmmoCost"])
                self.Range = str(character["Range"])
                self.RegenCost = str(character["RegenCost"])
                self.CollectionTexture = character["CollectionTexture"]
                self.FamilyName = character["FamilyName"]
                self.PersonalName = character["PersonalName"]
                self.School = character["School"]
                self.Club = character["Club"]
                self.SchoolYear = character["SchoolYear"]
                self.CharacterAge = character["CharacterAge"]
                self.Birthday = character["Birthday"]
                self.Equipment = character["Equipment"]
                self.StreetBattleAdaptation = character["StreetBattleAdaptation"]
                self.OutdoorBattleAdaptation = character["OutdoorBattleAdaptation"],
                self.BulletType = character["BulletType"]
                self.ArmorType = character["ArmorType"]
                self.WeaponType = character["WeaponType"]
                self.Position = character["Position"]
                self.Skills = character["Skills"]
                

        
        