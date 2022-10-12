import random, asyncio, aiosqlite
from datetime import datetime
from random import randint

import discord
from discord import ui 
from discord import app_commands, Member, Interaction
from discord.ext import commands

from data.user_data import morning
from data.hug_data import give, receive
from data.version import version

from utility.utils import defaultEmbed


class MainCog(commands.Cog, name='main'):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        user_id = message.author.id
        user = self.bot.get_user(message.author.id)
        morning_list = ['早安呀...', '早安喔...', '早安...',
                        '早安安...', '早安', '早', '早...', '早呀...', '早喔...']
        noon_list = ['午安呀...', '午安喔...', '午安安...', '午安', '午', '午安...', '午...']
        night_list = ['晚安呀...', '晚安喔...', '晚安安...', '晚安', '晚安...', '晚', '晚...']
        now = datetime.now()

        if message.author.bot or message.author.id == 427346531260301312:
            return
        else:
            if "早" in message.content or "午" in message.content or "晚" in message.content:
                if "奏" in message.content and "早" in message.content:
                    start = datetime(year=now.year, month=now.month,
                                    day=now.day, hour=5, minute=0, second=0, microsecond=0)
                    end = datetime(year=now.year, month=now.month, day=now.day,
                                hour=11, minute=59, second=0, microsecond=0)
                    if start <= now <= end:
                        author = morning.get(
                            message.author.id) or message.author.display_name
                        await message.reply(f'{author}{random.choice(morning_list)}')
                elif "奏" in message.content and "午" in message.content:
                    start = datetime(year=now.year, month=now.month, day=now.day,
                                    hour=12, minute=0, second=0, microsecond=0)
                    end = datetime(year=now.year, month=now.month, day=now.day,
                                hour=17, minute=59, second=0, microsecond=0)
                    if start <= now <= end:
                        author = morning.get(
                            message.author.id) or message.author.display_name
                        await message.reply(f'{author}{random.choice(noon_list)}')
                elif "奏" in message.content and "晚" in message.content:
                    author = morning.get(
                        message.author.id) or message.author.display_name
                    await message.reply(f'{author}{random.choice(night_list)}')

        love_list = ['奏不能喜歡你喔，我已經有真冬了///', '對不起... 我喜歡的是真冬...', '我不能對不起真冬...', '~~你有真冬那麼大嗎...~~']
        if "不" not in message.content and "奏" in message.content and "喜歡" in message.content:
            await message.reply(f'{random.choice(love_list)}')
            '''if message.author.id == 427346531260301312:
                await message.reply(f'奏不喜歡怪叔叔... <:angry_fbk:981195991137013830>')
            elif message.author.id == special['ayaakaa']['user_id']:
                await message.reply(f'奏最喜歡霞霞了！🤍')
            elif message.author.id == special['seria']['user_id']:
                await message.reply(f'雪... 🤍')
            else:    
                await message.reply(f'奏也愛你...')'''
        
        elif "召喚" in message.content and "奏" in message.content:
                await message.reply(f'召喚成功...')

    @app_commands.command(name='about', description='有關奏寶')
    async def about(self, interaction: discord.Interaction):
        embed = defaultEmbed(title="奏寶 • Kanade Bot",
                             description="**奏寶**是由**綾霞**製作的機器人")
        embed.set_author(name="奏寶", url="https://github.com/Ayaakaa/kanade_bot",
                         icon_url="https://i.imgur.com/oXEl8tP.jpg")
        embed.set_image(url="https://i.imgur.com/ZW5OWx8.png")
        embed.set_footer(text=f"奏寶 v{version} - by Ayaakaa@Seria Studios",
                     icon_url="https://imgur.com/HwcMqPS.png")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='say', description='用奏寶說話')
    @app_commands.checks.has_role('小雪團隊')
    async def say(self, i: discord.Interaction, message: str):
        await i.response.send_message('成功', ephemeral=True)
        await i.channel.send(message)

    @app_commands.command(name='leave-guild', description='leave-a-guild')
    @app_commands.checks.has_role('小雪團隊')
    async def guilds(self, i: discord.Interaction, guild_name: str):
        guild = discord.utils.get(self.bot.guilds, name=guild_name)
        if guild is None:
            await i.response.send_message("I don't recognize that guild.")
            return
        await guild.leave()
        await i.response.send_message(f"Left guild: {guild.name} ({guild.id})")
        
    @app_commands.command(name='hug', description='給某人一個擁抱')
    @app_commands.rename(member='某人')
    async def about(self, interaction: discord.Interaction, member: Member):
        gif_list = [
           'https://c.tenor.com/xXOZrdGr0-gAAAAd/hu-tao-qiqi-hu-tao-hugs.gif',
           'https://c.tenor.com/1_0ZOurJMSsAAAAd/genshin-impact-genshin.gif',
           'https://c.tenor.com/c0qkKNy2H6IAAAAd/darling-in-the-franxx-zhiro.gif',
           'https://cdn.weeb.sh/images/ryCG-OatM.gif',
           'https://c.tenor.com/Ms-P5bOXpXEAAAAC/lycoris-recoil-anime-hug.gif'
        ]
        img_list = [
           'https://cdn.donmai.us/original/f8/55/f855e1a9c5c64f7eaf3382d4858ea6b5.png',
           'https://i.ytimg.com/vi/wpMHed9_BA8/maxresdefault.jpg',
           'https://cdn.donmai.us/sample/5d/f6/sample-5df6a4a93008f4a5a3b1763ad86c306a.jpg',
           'https://i.redd.it/9ei1kxfgwnz61.png',
           'https://pbs.twimg.com/media/FD5KuL9VEAIbJ4Y.jpg',
           'https://static.zerochan.net/Hoshino.Ichika.%28Project.Sekai%29.full.3182755.png',
           'https://i.imgur.com/rLR2WUb.jpg',
           'https://i.pinimg.com/originals/50/c7/70/50c7709bfa5b3f67468fbd4b2e50f850.png',
           'https://cdn.discordapp.com/attachments/970929147985690626/1007586051784724500/illust_98340928_20220721_213342.jpg',
           'https://cdn.discordapp.com/attachments/970929147985690626/1007585997200035981/illust_96311763_20220812_172744.jpg'
            ]
        if interaction.user.id == member.id:
            await interaction.response.send_message('不要抱自己好嗎...')
            
            embed = defaultEmbed(title=f'那麼... ',
                                description=f'**奏寶給你一個抱抱吧！**')
            embed.set_image(url=f'{random.choice(gif_list)}')
            if receive.get(member.id) == None:
                receive[member.id] = 1
            else:    
                receive[member.id] = receive[member.id] + 1
            receive_hug = receive.get(interaction.user.id)
            if receive_hug == None: receive_hug = 0
            embed.set_footer(text=f'你總共收到了{receive_hug}個擁抱', icon_url=member.avatar)
            await interaction.followup.send(embed=embed)
            
           
        else:
            if give.get(interaction.user.id) == None:
                give[interaction.user.id] = 1
            else:    
                give[interaction.user.id] = give[interaction.user.id] + 1
                
            if receive.get(member.id) == None:
                receive[member.id] = 1
            else:    
                receive[member.id] = receive[member.id] + 1
            
            random_int = randint(1, 100)   
            
            embed = defaultEmbed(title=f'**抱抱！**',
                                description=f'**{interaction.user.display_name}給了{member.display_name}一個擁抱**')
            if random_int <= 70: embed.set_image(url=f'{random.choice(gif_list)}')
            elif random_int > 70: embed.set_image(url=f'{random.choice(img_list)}')
            receive_hug = receive.get(interaction.user.id)
            if receive_hug == None: receive_hug = 0
            embed.set_footer(text=f'{interaction.user.display_name}總共送出了{give.get(interaction.user.id)}個擁抱，並收到了{receive_hug}個擁抱', icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed)
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MainCog(bot))
