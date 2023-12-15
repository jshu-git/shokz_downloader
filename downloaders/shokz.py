from aiohttp import ClientSession
from os       import makedirs
from aiofiles import open as open_async

class Shokz:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.session     = ClientSession()

    async def close_session(self):
        await self.session.close()

    async def get_download_url(self, link):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        payload = {'url': link, 'aFormat': 'mp3', 'filenamePattern': 'basic', 'dubLang': False, 'isAudioOnly': True, 'isNoTTWatermark': True, 'disableMetadata': True }
        async with self.session.post('https://co.wuk.sh/api/json', headers=headers, json=payload) as response:
            result = await response.json()
            return result['url']

    async def download_url(self, url, filename):
        print(f'Downloading: {filename}')

        async with self.session.get(url, allow_redirects=True) as response:
            # make download folder
            download_folder = f'./downloads/{self.folder_name}'
            makedirs(download_folder, exist_ok=True)

            # download into folder
            async with open_async(f'{download_folder}/{filename}', 'wb') as f_out:
                await f_out.write(await response.read())
            print(f'Downloaded: {self.folder_name}/{filename}')

    async def get_default_filename(self, url):
        async with self.session.get(url, allow_redirects=True) as response:
            content_disposition = response.headers.get('content-disposition')
            filename            = content_disposition.split('"')[1]
            return filename