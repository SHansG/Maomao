import discord
import math
from discord.ext import commands
from voiceplayer import VoiceState, YTDLError, YTDLSource
from voiceplayer.utils.song_scrapper import Song_Scrapper


class Song_Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scrapper=Song_Scrapper()

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.hybrid_command(name='join', invoke_without_subcommand=True, help='Tells the bot to join the voice channel')
    async def _song_title(self, ctx: commands.Context, *, search: str):
        """Gets song title from spotify url."""
        title=self.scrapper.get_song_title(search)
        if title is None:
            title="URL not supported"
        ctx.send(title)