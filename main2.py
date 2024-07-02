from os import path
from argparse import ArgumentParser
from pathlib import Path
from shutil import copy
from send2trash import send2trash
from subprocess import call


if __name__ == "__main__":
    # parse args
    parser = ArgumentParser(
        description="python copy_only.py -s ~/Desktop/<folder>",
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
        raise Exception(f"{arg} does not exist")
    if not destination.is_dir():
        raise Exception(f"{arg} is not a directory")

    # create dir with name
    source = Path(args.name)
    (source).mkdir(parents=True, exist_ok=True)

    # run spotdl in dir
    status = call(f"spotdl download {args.link}", cwd=source, shell=True)

    # create destination folder with the source basename
    (destination / source.name).mkdir(parents=True, exist_ok=True)

    # copy files to destination in numerical order
    files = [f.name for f in source.iterdir() if not f.name.startswith(".")]
    files.sort(key=lambda f: f.split(" ")[0])  # 1 file.mp3, 2 file.mp3, etc.
    for name in files:
        source_file = source / name
        dest_file = destination / source.name / name
        print(f"copying: {name}")
        copy(source_file, dest_file)

    # remove source
    send2trash(str(source))
