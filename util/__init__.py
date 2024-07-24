from pathlib import Path
from shutil import copy
from time import sleep
from natsort import natsorted


def validate_paths(paths: list[Path]) -> None:
    for path in paths:
        if not path.exists():
            raise Exception(f"{args.destination} does not exist")
        if not path.is_dir():
            raise Exception(f"{args.destination} is not a directory")


# currently assumes numerical order
def copy_files(source: Path, destination: Path) -> None:
    files = [f.name for f in source.iterdir()]
    for name in natsorted(files):
        source_file = source / name
        dest_file = destination / source.name / name
        print(f"copying: {name}")
        copy(source_file, dest_file)
        sleep(0.1)
