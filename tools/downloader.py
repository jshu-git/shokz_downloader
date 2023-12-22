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
        self.unavailable = []

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
        If the link causes an invalid request, it's added to the unavailable list, which is later used to retry the download with a different link.
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
                try:
                    return result['url']
                except KeyError as e:
                    unavailable = 'unavailable' in result.get('text')
                    if unavailable:
                        print(f'<get_download_url()>: {link} is unavailable')
                        self.unavailable.append(link)
                        return None
                    else:
                        await self.close_session()
                        raise(KeyError(f'<get_download_url()>: {result}'))

    async def write(self, content, filename):
        '''
        This function saves the given content (a .mp3 file) with the given filename to the save path.
        '''
        if not path.exists(self.save_path):
            makedirs(self.save_path)
        async with open_async(path.join(self.save_path, filename), 'wb') as f_out:
            await f_out.write(content)

    async def get_default_filename(self, response):
        '''
        This function returns the default filename of the response.
        '''
        content_disposition = response.headers.get('content-disposition')
        filename            = content_disposition.split('"')[1]
        # remove all special characters, i.e. \udcb0, \udcc9, etc.
        filename            = ''.join([c for c in filename if ord(c) < 128])
        return filename
