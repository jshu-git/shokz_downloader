from os               import path
from shutil           import rmtree
from asyncio          import run as run_async, gather, create_task, sleep as sleep_async
from pytube           import Playlist

from tools.parser     import parse
from tools.downloader import Downloader
from tools.shokz      import Shokz

async def _download_async(downloader: Downloader, index, link):
    '''
    1. This function first sends a POST request to retrieve a url of a .mp3 file.
    2. It then sends a GET request to that url to download the .mp3 file and its information (such as its filename).
    3. It then saves the file to a folder.
    The filename is prepended with an index (if it was a playlist download) to preserve the order of the files. This is later used to copy the files in order.
    '''
    url = await downloader.get_download_url(link)
    if url:
        response, content = await downloader.get_response(url)
        filename          = await downloader.get_default_filename(response)
        await downloader.write(content, f'{index} {filename}')

async def main_async(save_path, links):
    '''
    This function downloads .mp3 files (asynchronously) to a folder.
    It staggers the start of each download to mitigate rate limiting.
    It returns a list of links that were unavailable so that they can be retried.
    '''
    downloader = Downloader(save_path)
    tasks      = []

    for index, link in enumerate(links, start=1):
        if index > 0:
            await sleep_async(1)
        tasks.append(create_task(_download_async(downloader, index, link)))
    await gather(*tasks)

    if downloader.unavailable:
        await downloader.close_session()
        return downloader.unavailable
    await downloader.close_session()

def copy_to_shokz(args, save_path):
    '''
    This function copies the locally downloaded files to the Shokz device. It then removes the local files.
    '''
    shokz = Shokz(volume_path=args.shokz)
    shokz.create_folder(args.name)
    shokz.copy_files(source_folder=save_path)
    rmtree(save_path)

if __name__ == '__main__':
    args        = parse()
    save_path   = path.join(path.expanduser(args.downloads), args.name) # i.e. /Users/username/Downloads/Daniel Caesar - Freudian
    links       = [link for link in Playlist(args.url)]
    unavailable = run_async(main_async(save_path, links))

    while unavailable:
        new_links = []
        print(f'\nthese links were unavailable: {unavailable}')
        for link in unavailable:
            new_link = input(f"enter a new link to retry for '{link}': ")
            new_links.append(new_link)
        unavailable = run_async(main_async(save_path, new_links))

    if args.shokz:
        print(f"\nfinished all downloads. about to move '{save_path}'' to Shokz device: '{args.shokz}'")
        input('make any changes to the files now if needed. then press Enter to continue...')
        copy_to_shokz(args, save_path)
        print('finished!')
