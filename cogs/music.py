import asyncio
import os
from dotenv import load_dotenv
import wavelink
from wavelink.ext import spotify

from discord import Interaction, app_commands
from discord.ext import commands
from utility.apps import musicApp
from utility.modules import errEmbed


load_dotenv()


class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host="127.0.0.1",
            port=2333,
            password=os.getenv("lavalink"),
            spotify_client=spotify.SpotifyClient(
                client_id="5f86059662e84a53b79454457f923fe0",
                client_secret="30812d67a6ab40419ca7d4d228a956ba",
            ),
        )

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self, player: wavelink.Player, track: wavelink.Track, reason
    ):
        if self.bot.repeat:
            await player.play(track)
        elif self.bot.prev:
            await player.play(player.queue.history[-2])
            player.queue.history.pop()
        else:
            if not player.queue.is_empty:
                await player.play(player.queue.get())
        try:
            await self.bot.wait_for("wavelink_track_start", timeout=300)
        except asyncio.TimeoutError:
            await player.disconnect()

    @app_commands.command(name="music", description="播放音樂")
    async def music(self, i: Interaction):
        if i.user.voice is None:
            return await i.response.send_message(
                embed=errEmbed().set_author(
                    name="請在語音台中使用此指令", icon_url=i.user.display_avatar.url
                ),
                ephemeral=True,
            )
        if not i.guild.voice_client:
            player: wavelink.Player = await i.user.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            player: wavelink.Player = i.guild.voice_client
        if player.channel.id != i.user.voice.channel.id:
            if player.is_playing():
                return await i.response.send_message(
                    embed=errEmbed(
                        message="你跟目前奏寶所在的語音台不同,\n且奏寶目前正在為那邊的使用者播歌\n請等待至對方播放完畢"
                    ).set_author(name="錯誤", icon_url=i.user.display_avatar.url),
                    ephemeral=True,
                )
            else:
                await player.disconnect()
                player: wavelink.Player = await i.user.voice.channel.connect(
                    cls=wavelink.Player
                )
        await i.response.defer()
        await musicApp.return_music_embeds(i, player)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MusicCog(bot))
