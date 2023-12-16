from os               import path
from asyncio          import run as run_async, gather, create_task, sleep as sleep_async
from pytube           import Playlist

from tools.parser     import parse
from tools.downloader import Downloader

async def _download_async(downloader: Downloader, index, link):
    url               = await downloader.get_download_url(link)
    response, content = await downloader.get_response(url)
    filename          = await downloader.get_default_filename(response)
    filename          = f'{index} {filename}' if index else filename # prepend index if playlist
    await downloader.save_download(content, filename)

async def main_async(save_path, links):
    downloader = Downloader(save_path)
    tasks      = []

    # single download
    if len(links) == 1:
        task = create_task(_download_async(downloader, 0, links[0]))
        tasks.append(task)
    # playlist download
    else:
        for index, link in enumerate(links, start=1):
            # stagger downloads after the first
            if index > 1:
                await sleep_async(1)
            task = create_task(_download_async(downloader, index, link))
            tasks.append(task)
    await gather(*tasks)
    await downloader.close_session()

if __name__ == '__main__':
    args      = parse()
    save_path = path.join(path.expanduser(args.downloads), args.name) # i.e. ~/Downloads/Daniel Caesar - Freudian
    try:
        links = [link for link in Playlist(args.url)]
    except KeyError:
        links = [args.url]

    # for testing
    # save_path = 'downloads'
    # links     = [
    #     'https://youtu.be/--I1pw11z1A',
    #     'https://www.youtube.com/watch?v=ee1RmJV9VaA',
    #     'https://www.youtube.com/watch?v=5HlRwXxK3S0',
    # ]

    run_async(main_async(save_path, links))