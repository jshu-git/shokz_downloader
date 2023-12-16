from os     import makedirs, path, listdir
from shutil import copy

class Shokz:
    def __init__(self, volume_path):
        self.volume_path = volume_path

    def create_folder(self, name):
        '''
        This function creates a folder on the Shokz device with the given name.
        '''
        folder_path = path.join(self.volume_path, name)
        makedirs(folder_path, exist_ok=True)

    def copy_files(self, source_folder):
        '''
        This function copies the .mp3 files from the given folder to the Shokz device.
        The files are copied over in numerical order to preserve order.
        '''
        base  = path.basename(source_folder)
        files = [f for f in listdir(source_folder) if f.endswith('.mp3')]
        # file names should be in the format: '1 file.mp3', '2 file.mp3', etc.
        files.sort(key=lambda f: int(f.split(' ')[0]))

        print(f'copying files from ({source_folder}) to ({path.join(self.volume_path, base)})')
        for filename in files:
            source_file = path.join(source_folder, filename)
            dest_file   = path.join(self.volume_path, base, filename)
            print(f'copying: {filename}')
            copy(source_file, dest_file)
            print(f'copied: {filename}')
