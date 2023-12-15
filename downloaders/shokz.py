from os       import makedirs
from json     import dumps
from requests import post, get

class Shokz:
    def __init__(self, folder_name):
        self.folder_name = folder_name

    def get_download_url(self, link):
        """
        This function sends a post request to https://cobalt.tools/ and returns the download link url.
        """
        headers  = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        payload  = {'url': link, 'aFormat': 'mp3', 'filenamePattern': 'basic', 'dubLang': False, 'isAudioOnly': True, 'isNoTTWatermark': True, 'disableMetadata': True}
        response = post('https://co.wuk.sh/api/json', headers=headers, data=dumps(payload))
        dict     = response.json()
        print(dict)
        return dict['url']

    def download_url(self, url, filename):
        """
        This function downloads the file from the url. It saves it to a local downloads folder with the specified filename.
        """
        print(f'Downloading: {filename}')
        response = get(url, allow_redirects=True)

        download_folder = f'./downloads/{self.folder_name}'
        # make folder
        try:
            makedirs(download_folder)
        except FileExistsError:
            pass
        # download into folder
        with open(f'{download_folder}/{filename}', 'wb') as f:
            f.write(response.content)
        print(f'Downloaded: {self.folder_name}/{filename}')

    def get_default_filename(self, url):
        """
        This function returns the default filename from the response headers.
        """
        response            = get(url, allow_redirects=True)
        content_disposition = response.headers.get('content-disposition') # attachment; filename="together - redveil.mp3"
        filename            = content_disposition.split('"')[1]
        return filename
