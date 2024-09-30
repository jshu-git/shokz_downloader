from argparse import ArgumentParser
from pathlib import Path
from subprocess import call
from send2trash import send2trash

from util import validate_paths, copy_files


if __name__ == "__main__":
    # parse args
    parser = ArgumentParser(
        description='python main.py -n "album name" -l "spotify link" -d "destination folder"',
    )
    parser.add_argument(
        "-n",
        "--name",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--link",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--destination",
        default="/Volumes/OpenSwim",
    )
    args = parser.parse_args()
    name = args.name
    link = args.link
    destination = Path(args.destination)

    # validate
    validate_paths(paths=[destination])

    # create temp dir with album name
    temp = Path(name)
    (temp).mkdir(parents=True, exist_ok=True)

    # run spotdl in temp dir
    spotdl_args = [
        # main options
        "--audio {youtube-music,youtube}",
        # output options
        "--preload",
        '--output "{list-position} {title}.{output-ext}"',
        "--print-errors",
        "--skip-album-art",
    ]
    command = f'spotdl download "{link}" {' '.join(spotdl_args)}'
    print(f"running: {command}")
    try:
        status = call(command, cwd=temp, shell=True)
    except Exception as e:
        print(f"error: {e}")
        raise

    # create destination folder with the source basename
    (destination / temp.name).mkdir(parents=True, exist_ok=True)

    # copy files to destination in numerical order
    copy_files(source=temp, destination=destination)

    # remove source
    send2trash(str(temp))
