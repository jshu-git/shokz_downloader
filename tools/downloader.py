from os       import makedirs, path
from aiohttp  import ClientSession
from aiofiles import open  as open_async
from asyncio  import sleep as sleep_async

class Downloader:
    def __init__(self, save_path):
        self.save_path   = save_path
        self.session     = ClientSession()
        self.max_retries = 3
        self.retry_delay = 10

    async def close_session(self):
        await self.session.close()

    async def get_response(self, url):
        '''
        This function sends a GET request to the given url and returns the response and content.
        If the response status is 429 (rate limited), the function will retry the request after a delay.
        '''
        for attempt in range(1, self.max_retries + 1):
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
        '''
        This function sends a POST request to the https://co.wuk.sh/api/json API, which returns a url to a .mp3 file.
        '''
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        payload = {'url': link, 'aFormat': 'mp3', 'filenamePattern': 'basic', 'dubLang': False, 'isAudioOnly': True, 'isNoTTWatermark': True, 'disableMetadata': True }

        for attempt in range(1, self.max_retries + 1):
            async with self.session.post('https://co.wuk.sh/api/json', headers=headers, json=payload) as response:
                if response.status == 429:
                    print(f'<get_download_url()>: rate limited, retrying in {self.retry_delay} seconds. Attempt: {attempt}')
                    await sleep_async(self.retry_delay)
                    continue
                result = await response.json()
                return result['url']

    async def save_download(self, content, filename):
        '''
        This function saves the given content (an .mp3 file) with the given fileame to the save path.
        '''
        makedirs(self.save_path, exist_ok=True)
        async with open_async(path.join(self.save_path, filename), 'wb') as f_out:
            await f_out.write(content)

    async def get_default_filename(self, response):
        '''
        This function returns the default filename from the content-disposition header.
        '''
        content_disposition = response.headers.get('content-disposition')
        filename            = content_disposition.split('"')[1]
        return filename