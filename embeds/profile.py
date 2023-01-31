from modules.main import defaultEmbed

from sekai.sekai_modules.main import format_date
from sekai.sekai_modules.main import get_data
from sekai.user.profile.profile import UserProfile

from data.emoji_data import character_icons


async def user_profile_embed(import_id: str, server: str):
    user_id = import_id
    profile = UserProfile()
    await profile.get_profile(server=server, user_id=user_id)
   
    name = profile.name
    rank = profile.rank
    word = profile.word
    
    if word == None or word == '' : word = '此玩家並沒有設置簡介'       
    leader_id = profile.userDecks['leader']
    cards_info = profile.userCards
    status_convert = {
        'original': 'normal',
        'special_training': 'after_training'}
    
    for card in cards_info:
        if card['cardId'] == leader_id:
            card_id = card['cardId']
            default_image = card['defaultImage']
            status = status_convert[default_image]
            data = await get_data(server='jp', type='diff', path='main/cards.json')
            for card in data:
                if card_id == card['id']:
                    asset_bundle_name = card['assetbundleName']
                    break
            break
        
    profile_pic = f'https://asset.pjsekai.moe/startapp/thumbnail/chara/{asset_bundle_name}_{status}.png'
    creation_date = format_date(server='jp', seconds=int((1600218000000 + int(import_id) / 2 ** 22) + 25200000) // 1000)
    userCharacters = profile.userCharacters
    characters_ranks = ''
    count = 0
    
    for character in userCharacters:
        id = character['characterId']
        emoji = character_icons[f'chr_ts_90_{id}']
        level = character['characterRank']
        string = f'{emoji}: {level}'  
        characters_ranks += string
        characters_ranks += ' \u200b \u200b '
        if count >= 2: 
            characters_ranks += '\n'
            count = 0
        else: 
            count += 1
        
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