from aiohttp  import ClientSession
from os       import makedirs
from aiofiles import open as open_async
from asyncio  import sleep as sleep_async

class Downloader:
    def __init__(self, save_path):
        self.save_path = save_path
        self.session       = ClientSession()
        self.retry_delay   = 10

    async def close_session(self):
        await self.session.close()

    async def get_response(self, url):
        for attempt in range(1, 4):
            async with self.session.get(url, allow_redirects=True) as response:
                if response.status == 429:
                    print(f'<get_response()>: rate limited, retrying in {self.retry_delay} seconds. Attempt: {attempt}')
                    await sleep_async(self.retry_delay)
                    continue
                filename = await self.get_default_filename(response)
                print(f'downloading: {filename}')
                content = await response.read()
                print(f'downloaded: {filename}')
                return response, content

    async def get_download_url(self, link):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        payload = {'url': link, 'aFormat': 'mp3', 'filenamePattern': 'basic', 'dubLang': False, 'isAudioOnly': True, 'isNoTTWatermark': True, 'disableMetadata': True }

        for attempt in range(1, 4):
            async with self.session.post('https://co.wuk.sh/api/json', headers=headers, json=payload) as response:
                if response.status == 429:
                    print(f'<get_download_url()>: rate limited, retrying in {self.retry_delay} seconds. Attempt: {attempt}')
                    await sleep_async(self.retry_delay)
                    continue
                result = await response.json()
                return result['url']

    async def save_download(self, content, filename):
        # make download folder
        makedirs(self.save_path, exist_ok=True)

        # download into folder with filename
        async with open_async(f'{self.save_path}/{filename}', 'wb') as f_out:
            await f_out.write(content)

    async def get_default_filename(self, response):
        content_disposition = response.headers.get('content-disposition')
        filename            = content_disposition.split('"')[1]
        return filename