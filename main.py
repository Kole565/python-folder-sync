from functions import *
from pprint import pp


# Arguments parsing

args = get_args()

# Getting files

folders_files_matrix = get_folders_files_matrix(args.dir)

# Filtering

filter_folders_files_matrix(
    folders_files_matrix, create_filter_by_name(
        args.filter_expression, expression_type=args.expression_type
    )
)
if args.verbose > 1:
    pp(f"Matrix: {folders_files_matrix}")
    print()

# Comparison

difference = get_difference(folders_files_matrix)
if args.verbose > 1:
    print(
        f"Difference (len {len(difference)}): {difference}",
        end="\n\n"
    )

# Transfer

for ind, (file_name, from_directory, to_directory) in enumerate(
    difference, start=1
):
    transfer(
        file_name, from_directory, to_directory,
        args.dry_run, bool(args.verbose)
    )
