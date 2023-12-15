from asyncio           import run as run_async, gather, ensure_future

from downloaders.shokz import Shokz as ShokzDownloader

async def main():
    shokz = ShokzDownloader(folder_name='Scaring the Hoes')
    links = ['https://youtu.be/--I1pw11z1A',
             'https://www.youtube.com/watch?v=ee1RmJV9VaA',
             'https://www.youtube.com/watch?v=5HlRwXxK3S0']

    tasks = []
    for index, link in enumerate(links):
        url      = await shokz.get_download_url(link)
        filename = await shokz.get_default_filename(url)
        task     = ensure_future(shokz.download_url(url, f'{index} {filename}'))
        tasks.append(task)
    await gather(*tasks)
    await shokz.close_session()

if __name__ == '__main__':
    run_async(main())