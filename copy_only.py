from os import path
from argparse import ArgumentParser
from pathlib import Path
from shutil import copy, rmtree
from send2trash import send2trash


if __name__ == "__main__":
    # parse args
    parser = ArgumentParser(
        description="python copy_only.py -s ~/Desktop/<folder>",
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

    # validate paths
    for arg in [args.source, args.destination]:
        path = Path(arg)
        if not path.exists():
            raise Exception(f"{arg} does not exist")
        if not path.is_dir():
            raise Exception(f"{arg} is not a directory")
    source = Path(args.source)
    destination = Path(args.destination)

    # create destination folder with the source basename
    (destination / source.name).mkdir(parents=True, exist_ok=True)
    # copy files over in numerical order
    files = [f.name for f in source.iterdir() if not f.name.startswith(".")]
    files.sort(key=lambda f: f.split(" ")[0])  # 1 file.mp3, 2 file.mp3, etc.
    for name in files:
        source_file = source / name
        dest_file = destination / source.name / name
        print(f"copying: {name}")
        copy(source_file, dest_file)

    # remove source
    send2trash(str(source))
