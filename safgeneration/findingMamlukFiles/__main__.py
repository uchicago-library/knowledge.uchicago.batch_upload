"""command-line script to find the mamluk CHOs that you care about right now
"""
from argparse import ArgumentParser
import csv
from os import getcwd, scandir
from os.path import basename, join, split, normpath
from os import _exit
from sys import stdout

def splitpath(path):
    parts = []
    path, tail = split(path)
    while path and tail:
        parts.append(tail)
        path, tail = split(path)
    parts.append(join(path, tail))
    parts.reverse()
    return [normpath(x) for x in parts]

def find_matching_directories(path, pattern_to_match=None):
    for n_item in scandir(path):
        if n_item.is_dir():
            yield from find_matching_directories(n_item.path, pattern_to_match=pattern_to_match)
        elif n_item.is_file():
            if pattern_to_match:
                if pattern_to_match in basename(n_item.path):
                    yield n_item.path
            else:
                yield n_item.path

def main():
    """the main function of the module
    """
    arguments = ArgumentParser()
    arguments.add_argument("data_location",
                           help="Location of the data to create SAFs from",
                           action="store", type=str)
    arguments.add_argument("-o", "--output",
                           help="File to write out output",
                           action='store', type=str, default=join(getcwd(), "matches.txt"))
    arguments.add_argument("-yp", "--year_pattern",
                           help="Year pattern in the form of YYYY where each Y is a number",
                           action='store', type=str, default=None)
    parsed = arguments.parse_args()
    try:
        generator = find_matching_directories(parsed.data_location,
                                              pattern_to_match=parsed.year_pattern)
        total_files_found = 0
        with open(parsed.output, "w+", encoding="utf-8") as write_file:
            writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["volume", "issue", "filename"])
            for n_file in generator:
                total_files_found += 1
                path_parts = splitpath(n_file)
                volume, issue = path_parts[4:6]
                record = [volume, issue, n_file]
                writer.writerow(record)
        stdout.write("{} files were added to the inventory file at {}\n".\
                     format(total_files_found, parsed.output))
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
