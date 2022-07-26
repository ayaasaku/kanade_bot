from datetime import timedelta, datetime
from discord.ext import commands
from tabulate import tabulate
from pytz import timezone
from jsondiff import diff
import asyncio, json, requests, discord

from discord import app_commands

from utility.utils import defaultEmbed

class LoopsCog(commands.Cog, name='loops'):

    def __init__(self, bot):
        self.bot = bot
        self.StartLoops() 
   
    def StartLoops(self):
        self.bot.loop.create_task(self.post_1m_cutoff_updates())
        self.bot.loop.create_task(self.post_1h_cutoff_updates())

    async def post_1m_cutoff_updates(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                from utility.apps.sekai.event_info import get_current_event_id
                event_id = await get_current_event_id()
            except Exception as e:
                print('Failed posting 2 minute data. Exception: ' + str(e))            
            if event_id:
                from utility.apps.sekai.time_formatting import is_event_active
                if(await is_event_active(event_id)):
                    from utility.apps.sekai.cutoff_formatting import get_cutoff_formatting
                    from utility.apps.sekai.database_formatting import get_cutoff_updates_channels
                    message = await get_cutoff_formatting()
                    ids = get_cutoff_updates_channels(1)
                    for i in ids:
                        channel = self.bot.get_channel(i)
                        if channel != None:
                            try:
                                await channel.send(message)
                            except (commands.BotMissingPermissions, discord.errors.NotFound, discord.errors.Forbidden): 
                                from utility.apps.sekai.database_formatting import rm_channel_from_cutoff_db
                                cutoff_updates_removal_notif = self.bot.get_channel(766718454635167775)
                                await cutoff_updates_removal_notif.send('Removing 1 minute updates from channel: ' + str(channel.name) + " in server: " + str(channel.guild.name))
                                rm_channel_from_cutoff_db(channel, 1)
                                
            timeStart = datetime.now()
            timeFinish = (timeStart + timedelta(minutes=1)).replace(second=0, microsecond=0).timestamp()
            timeStart = timeStart.timestamp()
            await asyncio.sleep(timeFinish - timeStart)

    async def post_1h_cutoff_updates(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            timeStart = datetime.now()
            timeFinish = (timeStart + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0).timestamp()            
            timeStart = timeStart.timestamp()
            await asyncio.sleep(timeFinish - timeStart)
            try:
                from utility.apps.sekai.event_info import get_current_event_id
                event_id = await get_current_event_id()
            except Exception as e:
                print('Failed posting 2 minute data. Exception: ' + str(e))            
            if event_id:
                from utility.apps.sekai.time_formatting import is_event_active
                if(await is_event_active(event_id)):
                    from utility.apps.sekai.cutoff_formatting import get_cutoff_formatting
                    from utility.apps.sekai.database_formatting import get_cutoff_updates_channels
                    message = await get_cutoff_formatting()
                    ids = get_cutoff_updates_channels(60)
                    for i in ids:
                        channel = self.bot.get_channel(i)
                        if channel != None:
                            try:
                                await channel.send(message)
                            except (commands.BotMissingPermissions, discord.errors.NotFound, discord.errors.Forbidden): 
                                from utility.apps.sekai.database_formatting import rm_channel_from_cutoff_db
                                cutoff_updates_removal_notif = self.bot.get_channel(766718454635167775)
                                await cutoff_updates_removal_notif.send('Removing 1 minute updates from channel: ' + str(channel.name) + " in server: " + str(channel.guild.name))
                                rm_channel_from_cutoff_db(channel, 60)


'''def setup(bot):
    bot.add_cog(loops(bot))'''
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LoopsCog(bot))