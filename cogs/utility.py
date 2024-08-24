from discord.ext import commands
import config

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.description = "Utility commands"
    
    @commands.hybrid_command(name='ping', aliases=(["pong"]))
    # @app_commands.describe(value="returns pong")
    async def ping(self, ctx: commands.Context):
        print("ping command called")
        # embed = discord.Embed(color=config.embed_color)
        # embed.add_field(name=f"{ctx.guild.id} Latency", value=f"{ctx.guild.id}:{self.bot.latency}")
        # embed.add_field(name="Field 1 Title", value="This is the value for field 1. This is NOT an inline field.", inline=False)
        # await ctx.send(embed=embed)
        await ctx.send(f"Latency: {self.bot.latency} ms")

    # @commands.hybrid_command(name='test', aliases=(["test"]))
    # # @app_commands.describe(value="returns pong")
    # async def test(self, ctx: commands.Context):
    #     embed = discord.Embed(color=config.embed_color)
    #     # embed.add_field(name=f"{ctx.guild.id} Latency", value=f"{ctx.guild.id}:{self.bot.latency}")
    #     embed.add_field(name="Field 1 Title", value="This is the value for field 1. This is NOT an inline field.", inline=False)
    #     await ctx.send(embed=embed)
    #     # await ctx.send(f"Latency: {self.bot.latency} ms")

    # @commands.hybrid_command(name="clear_slash_commands", aliases=(["clear"]))
    # async def clear_commands(self):
    #     await self.bot.tree.clear_commands(guild="")
    #     await self.bot.tree.sync(guild="")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Utility(bot))