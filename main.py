from downloaders.shokz import Shokz as ShokzDownloader

if __name__ == '__main__':
    shokz = ShokzDownloader(folder_name='Scaring the Hoes')

    links = ['https://youtu.be/--I1pw11z1A']
    for index, link in enumerate(links):
        url      = shokz.get_download_url(link=link)
        filename = shokz.get_default_filename(url=url)
        shokz.download_url(url=url, filename=f'{index} {filename}')