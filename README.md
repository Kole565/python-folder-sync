# Folders Sync

## Description

A simple python script for syncing files between multiple folders.

## Usage

For this script you only need python.

```bash
python main.py -h

usage: Folders Sync [-h] [-d | --dry-run | --no-dry-run] [--filter-expression FILTER_EXPRESSION] [--expression-type {wildcard,regexp}] [-v] dir [dir ...]

Tool for files sync between folders. Utilise hashing for uniquness check.

positional arguments:
  dir                   Directories to sync.

options:
  -h, --help            show this help message and exit
  -d, --dry-run, --no-dry-run
                        Omit any real changes or not.
  --filter-expression FILTER_EXPRESSION
                        Wildcards or regexp to use for filtering. See exp_type.
  --expression-type {wildcard,regexp}
                        How to interpret filtering expression. Choices are: ['wildcard', 'regexp']. Note: regexp wasn't tested.
  -v, --verbose
```

## Examples

Copy all missing files from folder_1 to folder_2 and vice-versa.

```bash
python main.py ./folder_1 ./folder_2
```

Copy all pdfs from folder_1 to folder_2 and folder_3 and vice-versa.

```bash
python main.py ./folder_1 ./folder_2 ./folder_3 --filter-expression "*.pdf"
```

Copy all pdfs from folder_1 to folder_2 and folder_3 and vice-versa.

```bash
python main.py ./folder_1 ./folder_2 ./folder_3 --filter-expression "*.pdf"
```

Sync books between folders using regular expression. Dry run.

```bash
python main.py ./folder_1 ./folder_2 --filter-expression "^.*\.(fb2|epub|txt|pdf)$" --expression-type "regexp" -d
```

## Author

Stepanov Nikolay\
email: rjkz565rjkz565@gmail.com\
Feel free to ask any questions related to this repo.
