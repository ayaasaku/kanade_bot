import time, discord, asyncio
from discord import app_commands, Interaction
from discord.ext import commands
from discord.app_commands import Choice

from utility.utils import defaultEmbed
from utility.apps.sekai.user.profile import user_profile
from utility.apps.sekai.user.data_processing import *

class ProfileCog(commands.Cog, name='profile'):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='profile', description='查看一個玩家的帳戶')    
    #@app_commands.rename(user_id='玩家id')           
    async def profile(self, interaction: discord.Interaction):#, user_id: int): 
        user_id = 244775114281091084 
        if user_id == await get_user_game_data(user_id, 'userId', self.bot.session):
            name = await get_user_game_data(user_id, 'name', self.bot.session)
            id = user_id
            rank = await get_user_game_data(user_id, 'rank', self.bot.session)
            word = await get_user_profile(user_id, 'word', self.bot.session)
            twitter_id = await get_user_profile(user_id, 'twitterId', self.bot.session) 
            leader_id = await get_user_decks(user_id, 'leader', self.bot.session)
            img_url = await get_user_profile_pic(user_id, leader_id, self.bot.session)       

            name = 'ayaakaa'
            rank = 27
            word = 'hi'
            twitter_id = ''
            
            embed = defaultEmbed(title=f'**{name}**', description=f'「{word}」')
            #embed.set_thumbnail(url=img_url)
            #embed.add_field(name=f'等級：', value=f'{rank}', inline=False)
            #if twitter_id != None or len(twitter_id) >= 1: 
                #embed.add_field(name=f'Twitter：', value=f'{twitter_id}', inline=False)
            #embed.add_field(name=f'Id：', value=f'`{id}`', inline=False)
            interaction.response.defer()
            asyncio.sleep(0.1)
            interaction.followup.send(embed=embed)
            await interaction.response.send_message(embed=embed)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ProfileCog(bot))