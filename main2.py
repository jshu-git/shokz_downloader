from argparse import ArgumentParser
from pathlib import Path
from shutil import copy
from send2trash import send2trash
from subprocess import call
from time import sleep


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
    destination = Path(args.destination)  # /Volumes/OpenSwim
    if not destination.exists():
        raise Exception(f"{arg} does not exist")
    if not destination.is_dir():
        raise Exception(f"{arg} is not a directory")

    # create dir with name
    temp = Path(args.name)  # .../Logic - College Park
    (temp).mkdir(parents=True, exist_ok=True)

    # run spotdl in dir
    try:
        status = call(f"spotdl download {args.link}", cwd=temp, shell=True)
    except Exception as e:
        print(f"error: {e}")
        raise

    # create destination folder with the source basename
    (destination / temp.name).mkdir(
        parents=True, exist_ok=True
    )  # /Volumes/OpenSwim/Logic - College Park

    # copy files to destination in numerical order
    files = [f.name for f in temp.iterdir()]
    files.sort(key=lambda f: f.split(" ")[0])  # 1 file.mp3, 2 file.mp3
    for name in files:
        source_file = temp / name  # .../Logic - College Park/1 file.mp3
        dest_file = (
            destination / temp.name / name
        )  # /Volumes/OpenSwim/Logic - College Park/1 file.mp3
        print(f"copying: {name}")
        copy(source_file, dest_file)
        sleep(0.1)

    # remove source
    send2trash(str(temp))
