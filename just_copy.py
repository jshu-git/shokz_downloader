from os           import path

from tools.parser import parse_just_copy
from tools.shokz  import Shokz

if __name__ == '__main__':
    args  = parse_just_copy()
    shokz = Shokz(volume_path=args.shokz)
    shokz.create_folder(path.basename(args.folder))
    shokz.copy_files(source_folder=args.folder)
