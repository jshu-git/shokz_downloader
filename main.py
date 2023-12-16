from os               import path
from shutil           import rmtree
from asyncio          import run as run_async, gather, create_task, sleep as sleep_async
from pytube           import Playlist

from tools.parser     import parse
from tools.downloader import Downloader
from tools.shokz      import Shokz

async def _download_async(downloader: Downloader, index, link):
    '''
    This function first sends a POST request to retrieve a url of a .mp3 file.
    It then sends a GET request to that url to download the .mp3 file and its information (such as its filename).
    It then saves the file to a folder.
    The filename is prepended with an index (if it was a playlist download) to preserve the order of the files. This is later used to copy the files in order.
    '''
    url               = await downloader.get_download_url(link)
    response, content = await downloader.get_response(url)
    filename          = await downloader.get_default_filename(response)
    filename          = f'{index} {filename}' if index else filename # prepend index if playlist
    await downloader.save_download(content, filename)

async def main_async(save_path, links):
    '''
    This function downloads .mp3 files (asynchronously) to a folder.
    '''
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

def copy_to_shokz(args):
    '''
    This function copies the locally downloaded files to the Shokz device.
    It then removes the local files.
    '''
    shokz = Shokz(volume_path=args.shokz)
    shokz.create_folder(args.name)
    shokz.copy_files(source_folder=save_path)
    rmtree(save_path)

if __name__ == '__main__':
    args      = parse()
    save_path = path.join(path.expanduser(args.downloads), args.name) # i.e. /Users/username/Downloads/Daniel Caesar - Freudian
    try:
        links = [link for link in Playlist(args.url)]
    except KeyError:
        links = [args.url]

    run_async(main_async(save_path, links))

    if args.shokz:
        copy_to_shokz(args)