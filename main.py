from asyncio           import run as run_async, gather, create_task

from downloaders.shokz import Shokz

async def download(shokz: Shokz, link, index):
    url              = await shokz.get_download_url(link)
    filename         = await shokz.get_default_filename(url)
    indexed_filename = f'{index} {filename}'
    await shokz.download_url(url, indexed_filename)

async def main(shokz: Shokz, links):
    tasks = []
    # schedule downloads tasks concurrently for each link
    for index, link in enumerate(links):
        task = create_task(download(shokz, link, index))
        tasks.append(task)
    await gather(*tasks)
    await shokz.close_session()

if __name__ == '__main__':
    shokz = Shokz(folder_name='Scaring the Hoes')
    links = [
        'https://youtu.be/--I1pw11z1A',
        'https://www.youtube.com/watch?v=ee1RmJV9VaA',
        'https://www.youtube.com/watch?v=5HlRwXxK3S0',
    ]
    run_async(main(shokz=shokz, links=links))