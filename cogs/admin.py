import discord
from discord import app_commands, client, Interaction, utils
from discord.ext import commands

from utility.modules import is_ayaakaa, defaultEmbed

class AdminCog(commands.Cog, name='admin'):
    def __init__(self, bot):
        self.bot = bot
        
    def updateEmbed(self, description: str = ''):
        embed = discord.Embed(title=f'**奏寶 v{self.bot.version}**', description=description, color=0xBB6688)
        embed.set_author(name="奏寶", url="https://github.com/Ayaakaa/kanade_bot",
                            icon_url="https://i.imgur.com/oXEl8tP.jpg")
        embed.set_image(url="https://i.imgur.com/1SJ6Y0Y.jpg")
        embed.set_footer(text=f"奏寶 - by 綾霞 Ayaakaa",
                        icon_url="https://avatars.githubusercontent.com/u/80079457?v=4")
        return embed

    @app_commands.command(name='embed', description='embed')
    @app_commands.rename(
        description='embed-description', \
        cmd_1='cmd-1-name', cmd_1_des_ln_1='cmd-1-description', cmd_1_des_ln_2='cmd-1-description2', \
        cmd_2='cmd-2-name', cmd_2_des_ln_1='cmd-2-description', cmd_2_des_ln_2='cmd-2-description2', \
        cmd_3='cmd-3-name', cmd_3_des_ln_1='cmd-3-description', cmd_3_des_ln_2='cmd-3-description2'
        )
    async def update(self, interaction: discord.Interaction, description: str, \
        cmd_1: str = '', cmd_1_des_ln_1: str = '', cmd_1_des_ln_2: str = '', \
        cmd_2: str = '', cmd_2_des_ln_1: str = '', cmd_2_des_ln_2: str = '', \
        cmd_3: str = '', cmd_3_des_ln_1: str = '', cmd_3_des_ln_2: str = ''):
        is_ayaakaa_ = await is_ayaakaa(interaction)
        if is_ayaakaa_ == True:
            embed = self.updateEmbed(description=description)
            if len(cmd_1) >= 1:
                embed.add_field(name=cmd_1, value=f'{cmd_1_des_ln_1}\n{cmd_1_des_ln_2}', inline=False)
            if len(cmd_2) >= 1:
                embed.add_field(name=cmd_2, value=f'{cmd_2_des_ln_1}\n{cmd_2_des_ln_2}', inline=False)
            if len(cmd_3) >= 1:
                embed.add_field(name=cmd_3, value=f'{cmd_3_des_ln_1}\n{cmd_3_des_ln_2}', inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name='say', description='用奏寶說話')
    async def say(self, i: Interaction, message: str):
        is_ayaakaa_ = await is_ayaakaa(i)
        if is_ayaakaa_ == True:
            await i.response.send_message('成功', ephemeral=True)
            await i.channel.send(message)


    @app_commands.command(name='leave-guild', description='leave-a-guild')
    async def leave_guild(self, i: Interaction, guild_name: str='', guild_id: int=0):
        is_ayaakaa_ = await is_ayaakaa(i)
        if is_ayaakaa_ == True:
            if len(guild_name) >= 1:
                guild = utils.get(self.bot.guilds, name=guild_name)
            elif guild_id != 0:
                guild = utils.get(self.bot.guilds, id=guild_id)
            else:
                await i.response.send_message("Error")
                return
            if guild is None:
                await i.response.send_message("I don't recognize that guild.")
                return
            await guild.leave()
            await i.response.send_message(f"Left guild: {guild.name} ({guild.id})")
    
    @app_commands.command(name='guilds', description='guilds')
    async def guilds(self, interaction: discord.Interaction):
        is_ayaakaa_ = await is_ayaakaa(interaction)
        if is_ayaakaa_ == True:
            embed = defaultEmbed() 
            for guild in self.bot.guilds:
                embed.add_field(name=guild.name, value=guild.id, inline=False)          
            await interaction.response.send_message(embed=embed, ephemeral= True)
                
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))
    
    