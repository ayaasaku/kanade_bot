import aiohttp

from data.emoji_data import character_icons
from sekai.sekai_modules.main import format_date
from sekai.sekai_modules.main import get_data
from sekai.user.profile.profile import UserProfile
from modules.main import defaultEmbed


async def user_profile_embed(import_id: str, session: aiohttp.ClientSession):
    user_id = import_id
    profile = UserProfile()
    await profile.get_profile(user_id, session)
   
    name = profile.name
    rank = profile.rank
    word = profile.word
    if word == None : word = '此玩家並沒有設置簡介'       
    leader_id = profile.userDecks['leader']
    cards_info = profile.userCards
    status_convert = {
        'original': 'normal',
        'special_training': 'after_training'}
    for card in cards_info:
        if card['cardId'] == leader_id:
            asset_bundle_name = card.get('assetbundleName')
            default_image = card.get('defaultImage')
            status = status_convert[default_image]
    profile_pic = f'https://asset.pjsekai.moe/startapp/thumbnail/chara/{asset_bundle_name}_{status}.png'
    creation_date = await format_date(server='jp', seconds=int((1600218000000 + int(import_id) / 2 ** 22) + 25200000) // 1000)
    userCharacters = profile.userCharacters
    characters_ranks = ''
    for character in userCharacters:
        id = character['characterId']
        emoji = character_icons[f'chr_ts_90_{id}']
        level = character['characterRank']
        string = f'{emoji}: {level}\u200b'  
        characters_ranks += string
        
        embed = defaultEmbed(title=f'**{name}**', description=f'「{word}」')
        embed.set_thumbnail(url=profile_pic)
        embed.add_field(name=f'等級：', value=rank, inline=False)
        embed.add_field(name=f'創建日期：', value=f'{creation_date}', inline=False)

        embed2 = defaultEmbed(title=f'**角色等級**')
        embed2.description = characters_ranks
        
        embed_list = [embed, embed2]
        for embed in embed_list:
            embed.set_footer(text=f'玩家ID：{import_id}', icon_url=f'{profile_pic}')
        return embed_list



'''description = f'{character_list_emoji[0]} {character_list_level[0]} \u200b {character_list_emoji[1]} {character_list_level[1]} \u200b {character_list_emoji[2]} {character_list_level[2]}\n\
{character_list_emoji[3]} {character_list_level[3]} \u200b {character_list_emoji[4]} {character_list_level[4]} \u200b {character_list_emoji[5]} {character_list_level[5]}\n\
{character_list_emoji[6]} {character_list_level[6]} \u200b {character_list_emoji[7]} {character_list_level[7]} \u200b {character_list_emoji[8]} {character_list_level[8]}\n\
{character_list_emoji[9]} {character_list_level[9]} \u200b {character_list_emoji[10]} {character_list_level[10]} \u200b {character_list_emoji[11]} {character_list_level[11]}\n\
{character_list_emoji[12]} {character_list_level[12]} \u200b {character_list_emoji[13]} {character_list_level[13]} \u200b {character_list_emoji[14]} {character_list_level[14]}\n\
{character_list_emoji[15]} {character_list_level[15]} \u200b {character_list_emoji[16]} {character_list_level[16]} \u200b {character_list_emoji[17]} {character_list_level[17]}\n\
{character_list_emoji[18]} {character_list_level[18]} \u200b {character_list_emoji[19]} {character_list_level[19]} \u200b {character_list_emoji[20]} {character_list_level[20]}\n\
{character_list_emoji[21]} {character_list_level[21]} \u200b {character_list_emoji[22]} {character_list_level[22]} \u200b {character_list_emoji[23]} {character_list_level[23]}\n\
{character_list_emoji[24]} {character_list_level[24]} \u200b {character_list_emoji[25]} {character_list_level[25]}'
        embed2.description = description'''
