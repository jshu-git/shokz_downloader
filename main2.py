from argparse import ArgumentParser
from pathlib import Path
from shutil import copy
from send2trash import send2trash
from subprocess import call
from time import sleep


if __name__ == "__main__":
    # parse args
    parser = ArgumentParser(
        description='python main2.py -n "name" -l "link"',
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

    # validate
    destination = Path(args.destination)
    if not destination.exists():
        raise Exception(f"{args.destination} does not exist")
    if not destination.is_dir():
        raise Exception(f"{args.destination} is not a directory")

    # create dir with name
    temp = Path(args.name)
    (temp).mkdir(parents=True, exist_ok=True)

    # run spotdl in dir
    spotdl_args = [
        # main options
        "--audio {youtube-music,youtube}",
        # output options
        "--preload",
        '--output "{list-position} {title}.{output-ext}"',
        "--print-errors",
        "--skip-album-art",
    ]
    command = f'spotdl download "{args.link}" {' '.join(spotdl_args)}'
    print(f"running: {command}")
    try:
        status = call(command, cwd=temp, shell=True)
    except Exception as e:
        print(f"error: {e}")
        raise

    # create destination folder with the source basename
    (destination / temp.name).mkdir(parents=True, exist_ok=True)

    # copy files to destination in numerical order
    files = [f.name for f in temp.iterdir()]
    files.sort(key=lambda f: f.split(" ")[0])  # 1 file.mp3, 2 file.mp3
    for name in files:
        source_file = temp / name
        dest_file = destination / temp.name / name
        print(f"copying: {name}")
        copy(source_file, dest_file)
        sleep(0.1)

    # remove source
    send2trash(str(temp))
