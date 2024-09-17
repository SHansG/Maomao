import discord
from discord.ext import commands

import config

class HelpView(discord.ui.View):
    def __init__(self, bot: commands.Bot, author: discord.Member) -> None:
        super().__init__(timeout=60)

        self.author: discord.Member = author
        self.bot: commands.Bot = bot
        self.response: discord.Message = None
        self.categories: list[str] = [ name.capitalize() for name, cog in bot.cogs.items() if len([c for c in cog.walk_commands()])]

    async def on_error(self, error, item, interaction) -> None:
        return
    
    async def on_timeout(self) -> None:
        for child in self.children:
            if child.custom_id == "select":
                child.disabled = True
        try:
            await self.response.edit(view=self)
        except:
            pass
    
    async def interaction_check(self, interaction: discord.Interaction[discord.Client]) -> bool:
        return interaction.user == self.author
    
    def build_embed(self, category: str) -> discord.Embed:
        category = category.lower()
        if category == "news":
            embed = discord.Embed(title="Maomao help menu", url="test_url", color=config.settings.embed_color)
            embed.add_field(
                name=f"Available Categories: [{2 + len(self.categories)}]",
                value="```py\n👉 News\n2. Tutorial\n{}```".format("".join(f"{i}. {c}\n" for i, c in enumerate(self.categories, start=3))),
                inline=True
            )

            update = "Maomao is a simple, multirole bot. It's in early development phase."
            embed.add_field(name="📰 Information:", value=update, inline=True)
            embed.add_field(name="Get Started", value="```Join a voice channel and /play {Song/URL} a song. (Names, Youtube Video Links or Playlist links or Spotify links are supported on Vocard)```", inline=False)
            
            return embed

        embed = discord.Embed(title=f"Category: {category.capitalize()}", color=config.settings.embed_color)
        embed.add_field(name=f"Categories: [{2 + len(self.categorys)}]", value="```py\n" + "\n".join(("👉 " if c == category.capitalize() else f"{i}. ") + c for i, c in enumerate(['News'] + self.categorys, start=1)) + "```", inline=True)

        cog = [c for _, c in self.bot.cogs.items() if _.lower() == category][0]

        commands = [command for command in cog.walk_commands()]
        embed.description = cog.description
        embed.add_field(
            name=f"{category} Commands: [{len(commands)}]",
            value="```{}```".format("".join(f"/{command.qualified_name}\n" for command in commands if not command.qualified_name == cog.qualified_name))
        )

        return embed