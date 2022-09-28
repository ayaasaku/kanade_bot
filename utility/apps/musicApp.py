import asyncio
import datetime
import re
import random

import wavelink
from wavelink.ext import spotify

from typing import Any


from discord import ButtonStyle, Interaction, Member, Embed, SelectOption
from discord.ui import Button, Modal, Select, View, TextInput
from utility.utils import defaultEmbed, errEmbed



def music_dec(func):
    async def inner_function(*args, **kwargs):
        item_self = args[0]
        interaction = args[1]
        await func(*args, **kwargs)
        await return_music_embeds(interaction, item_self.view.player)

    return inner_function


class View(View):
    def __init__(self, author: Member, player: wavelink.Player):
        super().__init__()
        self.author = author
        self.player = player
        self.add_item(Prev(len(player.queue.history) < 2))
        if player.is_paused():
            self.add_item(Play(not player.is_playing()))
        else:
            self.add_item(Pause(not player.is_playing()))
        self.add_item(Next(not player.queue))
        self.add_item(Stop(not player.is_playing()))
        self.add_item(Clear(not player.queue))
        self.add_item(Repeat(not player.is_playing()))
        self.add_item(Shuffle(not player.queue))
        self.add_item(Disconnect())
        self.add_item(AddSong())
        self.add_item(Reload())

    async def interaction_check(self, i: Interaction) -> bool:
        check = i.user.id == self.author.id
        if not check:
            await i.response.send_message(
                embed=errEmbed(message="自己用 /music 來打開一個播放器").set_author(
                    name="你很懶餒", icon_url=i.user.display_avatar.url
                ),
                ephemeral=True,
            )
        return check

    async def on_error(self, i: Interaction, error: Exception, item) -> None:
        await i.channel.send(
            embed=errEmbed(message=f"```py\n{error}\n```").set_author(
                name="出錯了餒", icon_url=i.user.display_avatar.url
            )
        )


class Play(Button):
    def __init__(self, disabled: bool):
        super().__init__(
            style=ButtonStyle.blurple,
            row=1,
            emoji="<:play:1021592463552557086>",
            disabled=disabled,
        )

    @music_dec
    async def callback(self, i: Interaction) -> Any:
        self.view: View
        await i.response.defer()
        await self.view.player.resume()


class Pause(Button):
    def __init__(self, disabled: bool):
        super().__init__(
            style=ButtonStyle.blurple,
            row=1,
            emoji="<:pause:1021592461665116201>",
            disabled=disabled,
        )

    @music_dec
    async def callback(self, i: Interaction) -> Any:
        self.view: View
        await i.response.defer()
        await self.view.player.pause()


class Stop(Button):
    def __init__(self, disabled: bool):
        super().__init__(
            style=ButtonStyle.red,
            row=3,
            disabled=disabled,
            emoji="<:stop:1021592456225112075>",
        )

    @music_dec
    async def callback(self, i: Interaction) -> Any:
        self.view: View
        await i.response.defer()
        self.view.player.queue.clear()
        await self.view.player.stop()


class Next(Button):
    def __init__(self, disabled: bool):
        super().__init__(row=1, disabled=disabled, emoji="<:next:1021592457894445086>")

    async def callback(self, i: Interaction) -> Any:
        self.view: View
        await i.response.defer()
        await self.view.player.stop()
        for item in self.view.children:
            item.disabled = True
        await i.edit_original_response(view=self.view)
        await asyncio.sleep(2)
        await return_music_embeds(i, self.view.player)


class Prev(Button):
    def __init__(self, disabled: bool):
        super().__init__(row=1, disabled=disabled, emoji="<:prev:1021592459458904076>")

    async def callback(self, i: Interaction) -> Any:
        self.view: View
        await i.response.defer()
        for item in self.view.children:
            item.disabled = True
        await i.edit_original_response(view=self.view)
        current = self.view.player.track
        self.view.player.queue.put_at_front(current)
        i.client.prev = True
        await self.view.player.stop()
        await asyncio.sleep(2)
        i.client.prev = False
        await return_music_embeds(i, self.view.player)


class Repeat(Button):
    def __init__(self, disabled: bool):
        super().__init__(
            style=ButtonStyle.green,
            row=2,
            disabled=disabled,
            emoji="<:repeat_song:1021592454618689627>",
        )

    async def callback(self, i: Interaction) -> Any:
        self.view: View
        await i.response.defer()
        i.client.repeat = not i.client.repeat
        await return_music_embeds(i, self.view.player, repeat=i.client.repeat)


class Shuffle(Button):
    def __init__(self, disabled: bool):
        super().__init__(
            style=ButtonStyle.green,
            row=2,
            disabled=disabled,
            emoji="<:shuffle:1021592452693508148>",
        )

    @music_dec
    async def callback(self, i: Interaction) -> Any:
        self.view: View
        await i.response.defer()
        queue = list(self.view.player.queue)
        random.shuffle(queue)
        self.view.player.queue.clear()
        self.view.player.queue.extend(queue)


class Clear(Button):
    def __init__(self, disabled: bool):
        super().__init__(row=2, disabled=disabled, emoji="<:clear:1021592450516647966>")

    @music_dec
    async def callback(self, i: Interaction) -> Any:
        self.view: View
        await i.response.defer()
        self.view.player.queue.clear()


class Disconnect(Button):
    def __init__(self):
        super().__init__(
            style=ButtonStyle.red,
            row=3,
            emoji="<:disconnect:1021592448541130762>",
        )

    async def callback(self, i: Interaction) -> Any:
        self.view: View
        await i.response.defer()
        await self.view.player.disconnect()
        await i.delete_original_response()


class AddSong(Button):
    def __init__(self):
        super().__init__(
            style=ButtonStyle.blurple, row=3, emoji="<:add_song:1021592446477549598>"
        )

    async def callback(self, i: Interaction) -> Any:
        await i.response.send_modal(AddSongModal(self.view))


class AddSongModal(Modal):
    query = TextInput(
        label="歌曲連結或關鍵字", placeholder="請輸入歌曲連結或關鍵字", min_length=1, max_length=2000
    )

    def __init__(self, music_view: View):
        super().__init__(title="新增歌曲", custom_id="add_song_modal")
        self.music_view = music_view

    async def on_submit(self, i: Interaction) -> None:
        await i.response.defer()
        view = self.music_view
        for children in view.children:
            children.disabled = True
        query = self.query.value
        regex = re.compile(
            r"^(?:http|ftp)s?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        player: wavelink.Player = i.guild.voice_client
        if re.match(regex, query) is not None:  # query is a url
            if decoded := spotify.decode_url(query):
                if decoded["type"] is spotify.SpotifySearchType.unusable:
                    embed = errEmbed().set_author(
                        name="無效的 Spotify 連結", icon_url=i.user.display_avatar.url
                    )
                    await i.edit_original_response(
                        embed=embed, ephemeral=True, view=view
                    )
                elif decoded["type"] in (
                    spotify.SpotifySearchType.playlist,
                    spotify.SpotifySearchType.album,
                ):
                    async for partial in spotify.SpotifyTrack.iterator(
                        query=decoded["id"], partial_tracks=True, type=decoded["type"]
                    ):
                        player.queue.put(partial)
                    if not player.is_playing():
                        await player.play(first := player.queue[0])
                    embed = defaultEmbed().set_author(
                        name="已新增 Spotify 播放清單/專輯", icon_url=i.user.display_avatar.url
                    )
                    if hasattr(first, "thumb"):
                        embed.set_image(url=first.thumb)
                    await i.edit_original_response(embed=embed, view=view)
                else:
                    track = await spotify.SpotifyTrack.search(
                        query=decoded["id"], return_first=True
                    )
                    await player.play(track)
                    embed = (
                        defaultEmbed()
                        .set_author(
                            name="已新增 Spotify 歌曲", icon_url=i.user.display_avatar.url
                        )
                        .set_image(url=track.thumb)
                    )
                    await i.edit_original_response(
                        embed=embed,
                        view=view,
                    )
            elif "youtu.be" in query or "youtube" in query:
                if "list" in query:
                    try:
                        playlist: wavelink.YouTubePlaylist = (
                            await wavelink.NodePool.get_node().get_playlist(
                                wavelink.YouTubePlaylist, query
                            )
                        )
                    except wavelink.errors.LoadTrackError:
                        return await i.followup.send(
                            embed=errEmbed().set_author(
                                name="無效的 YouTube 播放清單連結",
                                icon_url=i.user.display_avatar.url,
                            ),
                            ephemeral=True,
                        )
                    embed = defaultEmbed()
                    embed.set_author(
                        name="已新增 Youtube 播放清單", icon_url=i.user.display_avatar.url
                    )
                    if not player.is_playing():
                        await player.play(playlist.tracks[0])
                        for track in playlist.tracks[1:]:
                            player.queue.put(track)
                        if hasattr(player.queue[0], "thumb"):
                            embed.set_image(url=player.queue[0].thumb)
                    else:
                        for track in playlist.tracks:
                            player.queue.put(track)
                        if hasattr(playlist.tracks[0], "thumb"):
                            embed.set_image(url=player.queue[0].thumb)
                    await i.edit_original_response(embed=embed, view=view)
                else:
                    if "&t=" in query:
                        position = re.search("&t=", query).start()
                        query = query[:position]
                    try:
                        track = await wavelink.YouTubeTrack.search(
                            query=query, return_first=True
                        )
                    except IndexError:
                        return await i.followup.send(
                            embed=errEmbed().set_author(
                                name="無效的 YouTube 歌曲連結",
                                icon_url=i.user.display_avatar.url,
                            ),
                            ephemeral=True,
                        )
                    if not player.is_playing():
                        await player.play(track)
                    else:
                        player.queue.put(track)
                    embed = (
                        defaultEmbed()
                        .set_author(
                            name="已新增 Youtube 歌曲", icon_url=i.user.display_avatar.url
                        )
                        .set_image(url=track.thumb)
                    )
                    await i.edit_original_response(
                        embed=embed,
                        view=view,
                    )
        else:  # query is not an url
            tracks = await wavelink.YouTubeTrack.search(query)
            options = []
            for track in tracks[:25]:
                options.append(
                    SelectOption(
                        label=track.title, description=track.author, value=track.uri
                    )
                )
            embed = defaultEmbed().set_author(
                name=f"關鍵字搜尋: {query}", icon_url=i.user.display_avatar.url
            )
            view.clear_items()
            view.add_item(ChooseSongSelect(options))
            return await i.edit_original_response(embed=embed, view=view)
        await asyncio.sleep(1.5)
        await return_music_embeds(i, player)

    async def on_error(self, i: Interaction, error: Exception) -> None:
        return await super().on_error(i, error)

    async def on_timeout(self) -> None:
        return await super().on_timeout()


class ChooseSongSelect(Select):
    def __init__(self, options: list[SelectOption]):
        super().__init__(placeholder="選擇想播放的歌曲", options=options)

    async def callback(self, i: Interaction) -> Any:
        await i.response.defer()
        for children in self.view.children:
            children.disabled = True
        player: wavelink.Player = i.guild.voice_client
        track = await wavelink.YouTubeTrack.search(self.values[0], return_first=True)
        if not player.is_playing():
            await player.play(track)
        else:
            player.queue.put(track)
        embed = defaultEmbed()
        embed.set_author(name="已新增 Youtube 歌曲", icon_url=i.user.display_avatar.url)
        embed.set_image(url=track.thumb)
        await i.edit_original_response(embed=embed, view=self.view)
        await asyncio.sleep(1.5)
        await return_music_embeds(i, player)

class Reload(Button):
    def __init__(self):
        super().__init__(emoji='<:reload:1021950356135100547>', row=3)
    
    async def callback(self, i: Interaction) -> Any:
        await i.response.defer()
        await return_music_embeds(i, i.guild.voice_client)

async def get_player_embed(player: wavelink.Player) -> Embed:
    embed = defaultEmbed()
    current = player.track
    if current is None:
        embed.title = "目前沒有正在播放的歌曲"
        embed.description = "點按下方的按鈕來新增歌曲"
    else:
        embed.title = current.info["title"]
        value = f"<:song_author:1021667652718055475> 歌手: {current.info['author']}\n<:song_link:1021667672225763419> 連結: {current.info['uri']}\n"
        if isinstance(current, wavelink.Track):
            value += f"{'<:livestream:1021580269108609025> 直播' if current.is_stream() else '<:video:1021580271641968700> 影片'}"
        embed.description = value
        if isinstance(current, wavelink.YouTubeTrack):
            embed.set_thumbnail(url=current.thumb)
    return embed


async def get_queue_embed(queue: wavelink.Queue, repeat: bool) -> Embed:
    embed = defaultEmbed()
    if queue.is_empty:
        embed.title = "空的待播放清單"
        embed.description = "點按下方的按鈕來新增歌曲"
    elif repeat:
        embed.title = "循環模式開啟中"
    else:
        desc = ""
        for index, song in enumerate(list(queue)[:10]):
            desc += f"{index+1}. {song.info['title']}\n"
        embed.title = "播放清單(前10首)"
        embed.description = desc
    return embed


async def return_music_embeds(
    i: Interaction, player: wavelink.Player, repeat: bool = False
) -> None:
    player_embed = await get_player_embed(player)
    queue_embed = await get_queue_embed(player.queue, repeat)
    view = View(i.user, player)
    await i.edit_original_response(embeds=[player_embed, queue_embed], view=view)
