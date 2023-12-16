from os           import path
from pytube       import Playlist
from asyncio      import run as run_async, gather, create_task, sleep as sleep_async

from tools.parser import parse
from tools.shokz  import Shokz

async def _download_async(shokz: Shokz, index, link):
    url               = await shokz.get_download_url(link)
    response, content = await shokz.get_response(url)
    filename          = await shokz.get_default_filename(response)
    filename          = f'{index} {filename}' if index else filename # prepend index if playlist
    await shokz.save_download(content, filename)

async def main_async(download_path, links):
    shokz = Shokz(download_path)
    tasks = []

    # single download
    if len(links) == 1:
        task = create_task(_download_async(shokz, 0, links[0]))
        tasks.append(task)
    # playlist download
    else:
        for index, link in enumerate(links, start=1):
            # stagger downloads after the first
            if index > 1:
                await sleep_async(1)
            task = create_task(_download_async(shokz, index, link))
            tasks.append(task)
    await gather(*tasks)
    await shokz.close_session()

if __name__ == '__main__':
    args          = parse()
    download_path = path.join(path.expanduser(args.downloads), args.name)
    try:
        links = [link for link in Playlist(args.url)]
    except KeyError:
        links = [args.url]

    # for testing
    # download_path = 'downloads'
    # links = [
    #     'https://youtu.be/--I1pw11z1A',
    #     'https://www.youtube.com/watch?v=ee1RmJV9VaA',
    #     'https://www.youtube.com/watch?v=5HlRwXxK3S0',
    # ]

    run_async(main_async(download_path=download_path, links=links))