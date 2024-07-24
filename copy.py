from argparse import ArgumentParser
from pathlib import Path
from send2trash import send2trash

from util import validate_paths, copy_files


if __name__ == "__main__":
    # parse args
    parser = ArgumentParser(
        description='python copy.py -s "source folder" -d "destination folder"',
    )
    parser.add_argument(
        "-s",
        "--source",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--destination",
        default="/Volumes/OpenSwim",
    )
    args = parser.parse_args()
    source = Path(args.source)
    destination = Path(args.destination)

    # validate
    validate_paths(paths=[source, destination])

    # create destination folder with the source basename
    (destination / source.name).mkdir(parents=True, exist_ok=True)

    # copy files to destination in numerical order
    copy_files(source=source, destination=destination)

    # remove source
    send2trash(str(source))
