from pytube  import Playlist
from asyncio import run as run_async, gather, create_task, sleep as sleep_async

from tools.shokz import Shokz

async def download(shokz: Shokz, index, link):
    url               = await shokz.get_download_url(link)
    response, content = await shokz.get_response(url)
    filename          = await shokz.get_default_filename(response)
    await shokz.download_url(content, filename=f'{index} {filename}')

async def main(folder_name, links):
    shokz = Shokz(folder_name=folder_name)
    tasks = []
    # stagger downloads
    for index, link in enumerate(links):
        await sleep_async(0.5)
        task = create_task(download(shokz, index, link))
        tasks.append(task)
    await gather(*tasks)
    await shokz.close_session()

if __name__ == '__main__':
    folder_name = 'Scaring the Hoes'
    playlist    = Playlist('https://www.youtube.com/playlist?list=PLyJihFoIZ6EgoxN0E27LJr-GtuJDt6NQH')
    links       = [link for link in playlist]
    run_async(main(folder_name=folder_name, links=links))