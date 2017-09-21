"""
"""
from argparse import ArgumentParser
import csv
from os import getcwd, listdir, scandir
from os.path import basename, dirname, join
from os import _exit

def main():
    """the main function of the module
    """
    arguments = ArgumentParser()
    arguments.add_argument("data_location", action="store",
                           type=str,
                           help="Location of the data to create SAFs from",
                          )
    arguments.add_argument("-o", "--output", help="File to write out output", action='store',
                           type=str, default=join(getcwd(), "matches.txt"))
    parsed = arguments.parse_args()

    try:
        dir_contents = scandir(parsed.data_location)
        with open(parsed.output, "w+", encoding="utf-8") as write_file:
            for n in dir_contents:
                if n.is_dir() and basename(n.path).startswith('MamlukStudiesReview'):
                    write_file.write("{}\n".format(n.path))
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
