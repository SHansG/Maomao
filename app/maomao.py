import discord
import sys
import os
from discord.ext import commands
import config
import traceback

config.init()

class Maomao(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_message(self, message: discord.Message, /) -> None:
        if message.author.bot or not message.guild:
            return False
        
        if self.user.id in message.raw_mentions and not message.mention_everyone:
            prefix = await self.command_prefix(self,message)
            if not prefix:
                return await message.channel.send("I don't have prefix set")
            await message.channel.send(f"My prefix is `{prefix}`")
        
        await self.process_commands(message)

    async def setup_hook(self):
        for module in os.listdir(f"{config.ROOT_DIR}/cogs"):
            if module.endswith('.py'):
                try:
                    await self.load_extension(f"cogs.{module[:-3]}")
                    # print(f"cogs.{module[:-3]}")
                    print(f"Registered {module[:-3]} command(s)")
                except Exception as e:
                    print(traceback.format_exc())

        synced = await self.tree.sync()
        print(f"Total synced command(s): {len(synced)}")

    async def on_ready(self):
        print("------------------")
        print(f"Logging As {self.user}")
        print(f"Bot ID: {self.user.id}")
        print("------------------")
        print(f"Discord Version: {discord.__version__}")
        print(f"Python Version: {sys.version}")
        print("------------------")

        config.tokens.client_id = self.user.id

    async def on_command_error(self) -> None:
        pass


class CommandCheck(discord.app_commands.CommandTree):
    
    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if not interaction.guild:
            await interaction.response.send_message("This command can only be used in guilds!")
            return False

        return await super().interaction_check(interaction)


async def get_prefix(bot, message: discord.Message):
    settings = config.get_settings(message.guild.id)
    return settings.get("prefix", config.settings.bot_prefix)

intents = discord.Intents.default()
intents.message_content = True if config.settings.bot_prefix else False
member_cache = discord.MemberCacheFlags(
    voice=True,
    joined=False
)

bot = Maomao(
    command_prefix=get_prefix,
    help_command=None,
    tree_cls=CommandCheck,
    activity=discord.Activity(type=discord.ActivityType.listening, name="Starting..."),
    case_insensitive=True,
    intents=intents
)

if __name__=="__main__":
    bot.run(config.tokens.token, log_handler=None)