import argparse
import hashlib
import os
import shutil
from fnmatch import fnmatch
import re


def get_args():
    parser = argparse.ArgumentParser(
        prog="Folders Sync",
        description="Tool for files sync between folders. "
        "Utilise hashing for uniquness check."
    )
    parser.add_argument(
        "dir", help="Directories to sync.", nargs="+"
    )
    parser.add_argument(
        "-d", "--dry-run", help="Omit any real changes or not.",
        action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        "--filter-expression",
        help="Wildcards or regexp to use for filtering. See exp_type.",
        default="*"
    )
    parser.add_argument(
        "--expression-type",
        help="How to interpret filtering expression. "
        "Choices are: ['wildcard', 'regexp']. "
        "Note: regexp wasn't tested.",
        choices=["wildcard", "regexp"],
        default="wildcard"
    )
    parser.add_argument('-v', '--verbose', action='count', default=0)

    args = parser.parse_args()

    if args.verbose:
        print("Got arguments: ", args, end="\n\n")

    return args


def get_folders_files_matrix(folders):
    # folders_files_matrix = {
    #     "path_to_dir_1": [file_1, file_2],
    #     "path_to_dir_2": [file_3],
    # }
    folders_files_matrix = {}

    for path_to_folder in folders:
        absolute_path_to_folder = os.path.abspath(path_to_folder)
        folders_files_matrix[absolute_path_to_folder] = []

    for path_to_folder in folders:
        absolute_path_to_folder = os.path.abspath(path_to_folder)

        for file_name in (
            file_name for file_name in os.listdir(path_to_folder)
            if os.path.isfile(os.path.join(path_to_folder, file_name))
        ):
            file_data = {
                "name": file_name,
                "hash": get_file_hash(
                    os.path.join(absolute_path_to_folder, file_name)
                )
            }

            folders_files_matrix[absolute_path_to_folder].append(file_data)

    return folders_files_matrix


def get_file_hash(path):
    hash_md5 = hashlib.md5()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def get_difference(folders_files_matrix):
    """Return list of operations data in format [file_name, from, to]."""
    difference = []

    for path_to_current_folder, files in folders_files_matrix.items():
        other_folders = {
            k: v for k, v in folders_files_matrix.items()
            if k != path_to_current_folder
        }
        for file_data in files:
            # Scan every other folder.
            for path_to_other_folder, files in other_folders.items():
                if file_data["hash"] not in [
                    file_data["hash"] for file_data in files
                ]:
                    # If file is absent in other folder.
                    difference.append((
                        file_data["name"], path_to_current_folder,
                        path_to_other_folder
                    ))

    return difference


def filter_folders_files_matrix(folders_files_matrix, filter_func):
    for path_to_folder, files in folders_files_matrix.items():
        folders_files_matrix[path_to_folder] = list(filter(filter_func, files))


def create_filter_by_name(expression, expression_type="wildcard"):
    def wildcard_filter(file_data):
        return fnmatch(file_data["name"], expression)

    def regexp_filter(file_data):
        return bool(re.match(expression, file_data["name"]))

    if expression_type == "wildcard":
        return wildcard_filter
    if expression_type == "regexp":
        return regexp_filter


def transfer(
    file_name, from_directory, to_directory,
    verbose=True, dry_run=True
):
    if not dry_run:
        shutil.copy2(os.path.join(from_directory, file_name), to_directory)

    if verbose > 1:
        print(
            f"Copy {file_name} from {os.path.join(from_directory, file_name)} "
            f"to {to_directory} {'(dry run)' if dry_run else ''}"
        )
