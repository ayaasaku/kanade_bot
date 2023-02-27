from modules.main import defaultEmbed, errEmbed

from blue_archive.info.students_info import StudentInfo
from blue_archive.info.localization_jp import LocalizationInfoJp
from blue_archive.info.localization_tw import LocalizationInfoTw
from blue_archive.modules.info import *

async def character_embed(character_id: int):
    student = StudentInfo()
    student.get_student_info(character_id)
    img = f'https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/icon/{base_info["CollectionTexture"]}.png'


    #名字
    names = base_info["FamilyName"] + base_info["PersonalName"] + "、"
    for name in student_list[str(student_id)]:
        names = names + name + "、"
    msg_list.append(names[:-1])

    #背景
    school = localization_tw_data["School"][base_info["School"]]
    school_jp = localization_jp_data["School"][base_info["School"]]
    club = localization_tw_data["Club"][base_info["Club"]]
    club_jp = localization_jp_data["Club"][base_info["Club"]]

    msg_list.append(f'学校:{school_jp}({school})\n社团:{club_jp}({club})\n'
                    f'{base_info["SchoolYear"]}  {base_info["CharacterAge"]}\n生日:{base_info["Birthday"]}')

    #属性
    bullet_types = {"Explosion":"爆破","Pierce":"穿甲","Mystic":"神秘"}
    equipment_types = {"Gloves":"手套","Bag":"包","Watch":"手表","Shoes":"鞋","Badge":"徽章",
                       "Necklace":"项链","Hat":"帽子","Hairpin":"发卡","Charm":"饰品"}
    armor_types = {"HeavyArmor":"重甲","LightArmor":"轻甲","Unarmed":"神秘甲"}
    equipments = ""
    for equipment in base_info["Equipment"]:
        equipments += (equipment_types[equipment] if equipment in equipment_types else equipment) + "、"

    adaptation = f'地形适应: 市街:{str(base_info["StreetBattleAdaptation"])} / 户外:{str(base_info["OutdoorBattleAdaptation"])} / 室内:{str(base_info["IndoorBattleAdaptation"])}\n'
    bullet_type = bullet_types[base_info["BulletType"]] if base_info["BulletType"] in bullet_types else base_info["BulletType"]
    armor_type = armor_types[base_info["ArmorType"]] if base_info["ArmorType"] in armor_types else base_info["ArmorType"]

    type = f'攻击类型: {bullet_type}\n护甲类型: {armor_type}\n武器类型: {base_info["WeaponType"]}\n位置: {base_info["Position"]}\n' \
           f'装备: {equipments[:-1]}'


    msg_list.append(adaptation+type)

    #面板
    StabilityPoint = str(base_info["StabilityPoint"])
    AttackPower1 = str(base_info["AttackPower1"])
    AttackPower100 = str(base_info["AttackPower100"])
    MaxHP1 = str(base_info["MaxHP1"])
    MaxHP100 = str(base_info["MaxHP100"])
    DefensePower1 = str(base_info["DefensePower1"])
    DefensePower100 = str(base_info["DefensePower100"])
    HealPower1 = str(base_info["HealPower1"])
    HealPower100 = str(base_info["HealPower100"])
    DodgePoint = str(base_info["DodgePoint"])
    AccuracyPoint = str(base_info["AccuracyPoint"])
    CriticalPoint = str(base_info["CriticalPoint"])
    CriticalDamageRate = str(int(base_info["CriticalDamageRate"]/100))+"%"
    AmmoCount = str(base_info["AmmoCount"])
    AmmoCost = str(base_info["AmmoCost"])
    Range = str(base_info["Range"])
    RegenCost = str(base_info["RegenCost"])

    msg_list.append(f"HP:{MaxHP1}→{MaxHP100}		攻击:{AttackPower1}→{AttackPower100}\n"
                    f"防御:{DefensePower1}→{DefensePower100}		治愈:{HealPower1}→{HealPower100}\n"
                    f"闪避:{DodgePoint}		命中:{AccuracyPoint}\n"
                    f"暴击:{CriticalPoint}		暴伤:{CriticalDamageRate}\n"
                    f"弹药:{AmmoCount}		耗弹:{AmmoCost}\n"
                    f"安定:{StabilityPoint}		范围:{Range}\n"
                    f"回费:{RegenCost}\n")


    #技能
    global parameters
    skill_desc = ""
    skills = base_info["Skills"]
    for skill in skills:
        skill_desc += skill["SkillType"] + "\n"
        skill_desc += skill["Name"]
        parameters = skill["Parameters"]
        if skill["SkillType"] == "ex":
            skill_desc += f' (Cost:{str(skill["Cost"][0])}→{str(skill["Cost"][-1])})'
            desc = re.sub(r'<\?(\d+)>', fmt_para_ex, skill["Desc"])
        else:
            desc = re.sub(r'<\?(\d+)>', fmt_para, skill["Desc"])
        desc = re.sub(r'<(\w):(\w+)>',fmt_desc,desc)
        skill_desc += "\n" + desc + "\n\n"

    msg_list.append(skill_desc)
    
