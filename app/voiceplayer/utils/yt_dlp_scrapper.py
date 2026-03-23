import yt_dlp
import asyncio
import functools

class VoiceError(Exception):
    pass

class YTDLError(Exception):
    pass

class YTDLSource:
    YTDL_OPTIONS = {
        'format': 'bestaudio[ext=webm]/bestaudio/best',
        'cachedir': False,
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
        'cookiefile': 'cookies.txt',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-nostdin -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -fflags +nobuffer -probesize 32k -analyzeduration 0 -user_agent "Mozilla/5.0"',
        'options': '-vn -loglevel warning -af aresample=async=1:min_hard_comp=0.100000:first_pts=0',
    }

    ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, data: dict):
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4] if date else None
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration'))) if data.get('duration') else None
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        # Perform a search using yt-dlp
        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError(f'Couldn\'t find anything that matches `{search}`')

        if 'entries' not in data:
            process_info = data
        else:
            # If the search returns multiple entries, take the first one
            process_info = next((entry for entry in data['entries'] if entry), None)
            if process_info is None:
                raise YTDLError(f'Couldn\'t find anything that matches `{search}`')

        webpage_url = process_info['webpage_url']

        # Extract full info from the video webpage URL
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError(f'Couldn\'t fetch `{webpage_url}`')

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = next((entry for entry in processed_info['entries'] if entry), None)
            if info is None:
                raise YTDLError(f'Couldn\'t retrieve any matches for `{webpage_url}`')

        # Return a new instance of YTDLSource with the extracted information
        return cls(info)
    
    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)
    

async def main():
    scrapped_name = 'Jefferson Airplane - Run Around'
    source = await YTDLSource.create_source(scrapped_name)
    print(f"{source.uploader} \
          \n{source.title} \
          \n{source.url}")

if __name__ == '__main__':
    asyncio.run(main())