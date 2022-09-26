import discord
import sentry_sdk

from utility.utils import errEmbed, log


async def global_error_handler(
    i: discord.Interaction, e: Exception | discord.app_commands.AppCommandError
):
    if isinstance(e, discord.app_commands.errors.CheckFailure):
        return
    log.warning(f"[{i.user.id}]{type(e)}: {e}")
    sentry_sdk.capture_exception(e)

    if isinstance(e, discord.errors.NotFound):
        if e.code in [10062, 10008]:
            embed = errEmbed(message='ERROR')
            embed.set_author(name=i.user.display_name,
                             icon_url=i.user.display_avatar.url)
    else:
        embed = errEmbed(message='error')
        embed.set_author(
            name=i.user.display_name,
            icon_url=i.user.display_avatar.url,
        )

    try:
        await i.response.send_message(
            embed=embed,
            ephemeral=True,
        )
    except discord.errors.InteractionResponded:
        await i.followup.send(
            embed=embed,
            ephemeral=True,
        )
    except discord.errors.NotFound:
        pass


class BaseView(discord.ui.View):
    async def interaction_check(self, i: discord.Interaction) -> bool:
        if not hasattr(self, "author"):
            return True
        if self.author.id != i.user.id:
            await i.response.send_message(
                embed=errEmbed().set_author(
                    name='ERROR',
                    icon_url=i.user.display_avatar.url,
                ),
                ephemeral=True,
            )
        return self.author.id == i.user.id

    async def on_error(self, i: discord.Interaction, e: Exception, item) -> None:
        await global_error_handler(i, e)

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

        try:
            await self.message.edit(view=self)
        except AttributeError:
            log.warning(
                f"[Edit View] Attribute Error: [children]{self.children} [view]{self}"
            )
        except discord.HTTPException:
            log.warning(
                f"[Edit View] HTTPException: [children]{self.children} [view]{self}"
            )
        except Exception as e:
            log.warning(f"[Edit View] Failed{e}")
            sentry_sdk.capture_event(e)

class BaseModal(discord.ui.Modal):
    async def on_error(self, i: discord.Interaction, e: Exception) -> None:
        log.warning(f"[Modal Error][{i.user.id}]: [type]{type(e)} [e]{e}")
        sentry_sdk.capture_exception(e)
        embed = errEmbed('ERROR')
        embed.set_author(
            name=i.user.display_name, icon_url=i.user.display_avatar.url
        )
        embed.set_thumbnail(url="https://i.imgur.com/4XVfK4h.png")

        try:
            await i.response.send_message(
                embed=embed,
                ephemeral=True,
            )
        except discord.InteractionResponded:
            await i.followup.send(
                embed=embed,
                ephemeral=True,
            )
        except discord.NotFound:
            pass
        
class BaseModal(discord.ui.Modal):
    async def on_error(self, i: discord.Interaction, e: Exception) -> None:
        await global_error_handler(i, e)