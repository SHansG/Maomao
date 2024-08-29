import os
from dotenv import load_dotenv

class Settings:
    def __init__(self, settings: dict) -> None:
        # self.invite_link = ""  # later put the link there
        self.nodes = settings.get("nodes", {})
        self.max_queue = settings.get("default_max_queue", 1000)
        self.bot_prefix = settings.get("prefix", "")
        self.activity = settings.get("activity", "")
        self.embed_color = int(settings.get("embed_color", "0x4b19bf"), 16)
        self.bot_access_user = settings.get("bot_access_user", [])
        self.emoji_source_raw = settings.get("emoji_source_raw", {})
        self.cooldowns_settings = settings.get("cooldowns", {})
        self.aliases_settings = settings.get("aliases", {})
        self.controller = settings.get("default_controller", {})
        self.ipc_server = settings.get("ipc_server", {})
        self.version = settings.get("version", "")
        self.settings_dict = settings


class TOKENS:
    def __init__(self) -> None:
        load_dotenv()

        self.token = os.getenv("DISCORD_TOKEN")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret_id = os.getenv("CLIENT_SECRET_ID")
        self.bug_report_channel_id = int(os.getenv("ERROR_REPORT_CHANNEL_ID"))
        self.spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.mongodb_name = os.getenv("MONGODB_NAME")
        self.mongodb_url = os.getenv("MONGODB_URL")