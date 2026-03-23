import discord
import config
from discord import app_commands
from discord.ext import commands

from views.help import HelpView

class Settings(commands.Cog, name="settings"):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.description = "This category is only available to admins."
    
    def get_settings(self, ctx: commands.Context) -> dict:
        settings = config.get_settings(ctx.guild.id)
        return settings
    
    @commands.hybrid_group(
        name="settings",
        aliases=["sett"],
        invoke_without_command=True
    )
    async def settings(self, ctx: commands.Context):
        view = HelpView(self.bot, ctx.author)
        embed = view.build_embed(self.qualified_name)
        view.response = await ctx.send(embed=embed, view=view)

    @settings.command(name="prefix", aliases=["pre"])
    @commands.has_permissions(manage_guild=True)
    # @commands.dynamic_cooldown(cooldown_check, commands.BucketType.guild)
    async def prefix(self, ctx: commands.Context, prefix: str):
        """Change default prefix for message commands"""
        old_prefix = config.settings.bot_prefix
        config.update_settings(ctx.guild.id, {"prefix":prefix})
        await ctx.send(f"changing prefix: {old_prefix} -> {prefix}")

    @settings.command(name='view', aliases=['v'])
    @commands.has_permissions(manage_guild=True)
    async def view(self, ctx: commands.Context) -> None:
        """Show bot's settings"""
        settings = self.get_settings(ctx)
        await ctx.send(f"```py\n{settings}```")
        # embed = discord.Embed(color=config.settings.embed_color)
        # embed.set_author(name=f"settingsMenu {ctx.guild.name}", icon_url=self.bot.user.display_avatar.url)
        # if ctx.guild.icon:
        #     embed.set_thumbnail(url=ctx.guild.icon.url)

        # embed.add_field(name='settingsTitle', value="".format(
        #     settings.get('prefix', config.settings.bot_prefix) or None,
        #     inline=True)
        # )

        # # perms = ctx.guild.me.guild_permissions
        # # embed.add_field(name='settingsPermTitle', value="settingsPermValue".format(
        # #     '<a:Check:941206936651706378>' if perms.administrator else '<a:Cross:941206918255497237>',
        # #     '<a:Check:941206936651706378>' if perms.manage_guild else '<a:Cross:941206918255497237>',
        # #     '<a:Check:941206936651706378>' if perms.manage_channels else '<a:Cross:941206918255497237>',
        # #     '<a:Check:941206936651706378>' if perms.manage_messages else '<a:Cross:941206918255497237>'), inline=False)
        # await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Settings(bot))