from discord.ext import commands
from tabulate import tabulate
from datetime import datetime, timedelta
from pytz import timezone
from tabulate import tabulate
import time, re, discord

from discord import app_commands

from utility.utils import defaultEmbed
from data.emoji_data import attributes
from data.translate_data import translate

class EventCog(commands.Cog, name='event'):
    def __init__(self, bot):
        self.bot = bot

    '''@commands.command(name='timeleft',
                      aliases=['tl'],
                      description="Provides the amount of time left (in hours) for an event",
                      help=".timeleft")'''
    @app_commands.command(name='timeleft', description='查看本期活動的剩餘時間')
    async def time_left(self, interaction: discord.Interaction):
        from utility.apps.sekai.event_info import get_event_end_time_jp, get_current_event_id_jp, get_event_name_jp, \
            get_event_start_time_jp, get_event_banner_name_jp
        from utility.apps.sekai.time_formatting import format_time, format_date, format_progress
        global event_id
        event_id = 0
        event_id = await get_current_event_id_jp()
        event_end_time = (await get_event_end_time_jp(event_id)) / 1000
        current_time = time.time()
        if current_time > event_end_time:
            await interaction.send("There's no active event!")
        else:
            event_end_date = await format_date(event_end_time * 1000)
            event_name = await get_event_name_jp(event_id)
            event_start_time = await get_event_start_time_jp(event_id)
            event_banner_name = await get_event_banner_name_jp(event_id)
            logo_url = f"https://minio.dnaroma.eu/sekai-assets/event/{event_banner_name}/logo_rip/logo.webp"
            banner_url = f"https://minio.dnaroma.eu/sekai-assets/home/banner/{event_banner_name}_rip/{event_banner_name}.webp"
            event_url = f'https://sekai.best/event/{event_id}'
            time_left = await format_time(event_end_time - current_time)
            event_prog = await format_progress(event_end_time, (event_start_time / 1000), current_time)
            embed = defaultEmbed(title=f'**{event_name}**')
            embed.set_thumbnail(url=logo_url)
            embed.set_image(url=banner_url)
            embed.add_field(name=f'剩餘時間', value=f'{time_left}', inline=False)
            embed.add_field(name=f'進度', value=f'{event_prog}', inline=False)
            embed.add_field(name=f'結束日期', value=f'{event_end_date}', inline=False)
            embed.add_field(name='更多資訊', value=event_url, inline=False)
            await interaction.response.send_message(embed=embed)

    '''@commands.command(name='event',
                      description='Posts event info',
                      help='event\n.event jp\n.event en 12\n.event en Lisa\n.event jp 一閃')'''
    @app_commands.command(name='event', description='查看本期活動的資訊')                 
    async def event(self, interaction: discord.Interaction):
        from utility.apps.sekai.event_info import get_event_name_jp, get_event_type_jp, get_current_event_id_jp, \
            get_event_bonus_attribute_jp, get_event_banner_name_jp, get_event_start_time_jp, get_event_end_time_jp, \
            get_event_bonus_characters_id_jp, get_event_bonus_characters_name_jp
        from utility.apps.sekai.time_formatting import format_date
        global event_id
        event_id = 0
        if event_id == 0:
            event_id = await get_current_event_id_jp()
        event_name = await get_event_name_jp(event_id)
        event_type = await get_event_type_jp(event_id)
        event_banner_name = await get_event_banner_name_jp(event_id)
        event_bonus_attribute = await get_event_bonus_attribute_jp()
        event_start_time = await format_date(await get_event_start_time_jp(event_id))
        event_end_time = await format_date(await get_event_end_time_jp(event_id))
        logo_url = f"https://minio.dnaroma.eu/sekai-assets/event/{event_banner_name}/logo_rip/logo.webp"
        banner_url = f"https://minio.dnaroma.eu/sekai-assets/home/banner/{event_banner_name}_rip/{event_banner_name}.webp"
        event_url = f'https://sekai.best/event/{event_id}'
        event_attribute_translated = translate['attributes'][str(event_bonus_attribute)]
        attribute_emoji = attributes[str(event_bonus_attribute)]
        event_type_translated = translate['event_type'][str(event_type)]
        event_bonus_characters_id_list = await get_event_bonus_characters_id_jp(event_id)
        event_bonus_characters_name_list = await get_event_bonus_characters_name_jp(event_bonus_characters_id_list)
        embed = defaultEmbed(title=f'**{event_name}**')
        embed.set_thumbnail(url=logo_url)
        embed.set_image(url=banner_url)
        embed.add_field(name='活動類型', value=event_type_translated, inline=False)  
        embed.add_field(name='加成屬性', value=f'{attribute_emoji} {event_bonus_attribute}\n<:placeholder:1001375846814203906> ({event_attribute_translated})', inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='加成角色', value=f'{event_bonus_characters_name_list[0]}，{event_bonus_characters_name_list[1]}\n{event_bonus_characters_name_list[2]}，{event_bonus_characters_name_list[3]}', inline=True)  
        embed.add_field(name='開始', value=event_start_time, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='結束', value=f'{event_end_time}', inline=True)
        #embed.add_field(name='\u200b', value='**時間**', inline=False)
        embed.add_field(name='更多資訊', value=event_url, inline=False)
        await interaction.response.send_message(embed=embed)


    '''valid_tiers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 4000, 5000, 10000, 20000,
                   30000, 40000, 50000, 100000}

    @commands.command(name='cutoff',
                      brief="cutoff info",
                      description="Posts cutoff info",
                      help=".cutoff (posts cutoff info for all tiers)\n.cutoff 100",
                      aliases=[f't{tier}' for tier in valid_tiers] +
                              [f't{tier // 1000}k' for tier in valid_tiers if tier % 1000 == 0])
    @app_commands.command(name='cutoff', description='Posts cutoff info')    
    @app_commands.rename(tier='tier')   
    async def cutoff(self, interaction: discord.Interaction, tier: str = '0'):
        command_name = f'cutoff {tier}'
        tier_regex = re.compile(r"t?\d+k?")

        def parse_tier(tier_arg):
            if tier_arg[0] == 't':
                tier_arg = tier_arg[1:]
            if tier_arg[-1] == 'k':
                return 1000 * int(tier_arg[:-1])
            return int(tier_arg)

        if tier_regex.fullmatch(command_name):
            if tier != '0':
                await interaction.followup.send(f"Tier already specified via alias")
                return
            tier = parse_tier(command_name)
        else:
            if not tier_regex.fullmatch(tier):
                await interaction.followup.send(f"Tier `{tier}` isn't recognized")
                return
            tier = parse_tier(tier)

        from utility.apps.sekai.cutoff_formatting import get_cutoff_formatting

        if tier == 0 or tier == 10:
            await interaction.followup.send(await get_cutoff_formatting(str(tier)))
        elif tier in self.valid_tiers:
            await interaction.followup.send(embed=await get_cutoff_formatting(str(tier)))
        else:
            await interaction.followup.send(f"Tier `{tier}` isn't supported")'''


'''def setup(bot):
    bot.add_cog(event(bot))'''
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventCog(bot))
