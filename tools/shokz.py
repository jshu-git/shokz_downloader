from os     import makedirs, path, listdir
from shutil import copy

class Shokz:
    def __init__(self, volume_path):
        self.volume_path = volume_path

    def create_folder(self, name):
        folder_path = path.join(self.volume_path, name)
        makedirs(folder_path, exist_ok=True)

    def copy_files(self, folder):
        files = [f for f in listdir(folder) if f.endswith('.mp3')]
        files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

        for name in files:
            source = path.join(folder, name)
            dest   = path.join(self.volume_path, path.basename(folder), name)
            print(f'copying: {name}')
            copy(source, dest)
            print(f'copied: {name}')

