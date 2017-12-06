from argparse import ArgumentParser
import csv
from os import getcwd, scandir
from os.path import basename, join, split, normpath, dirname, exists
from os import _exit
from sys import stdout
from xml.etree import ElementTree

def main():
    """the main function of the module
    """
    arguments = ArgumentParser()
    arguments.add_argument("index_file",
                           help="Location of the dissertation ProQuest data",
                           action="store", type=str)
    arguments.add_argument("spreadsheet",
                           help="Location of the dissertation spreadsheet defining which ones you want in this SAF",
                           action="store", type=str)
    arguments.add_argument("root",
                           help="Location of the dissertation index file",
                           action="store", type=str) 
    arguments.add_argument("-o", "--output",
                           help="Optional parameter to set output file location.",
                           action='store', default=join(getcwd(), 'matches.txt'))
    parsed = arguments.parse_args()
    try:
        index = csv.reader(open(parsed.index_file, "r", encoding="utf-8"),
                           delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        index_lines =[x for x in index]
        matches = []
        with open(parsed.spreadsheet, "r", encoding="utf-8") as read_file:
            reader = csv.reader(read_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            count = 0
            match_total = 0
            for row in reader:
                if count > 0:
                    record_title = row[6]
                    for index_record in index_lines:
                        length = len(index_record)
                        if length > 0:
                            index_title = index_record[0]
                            if index_title == record_title:
                                match_total += 1
                                object_dir = normpath(parsed.root) +\
                                 normpath(dirname(index_record[3]))
                                f = open(parsed.output, "a+", encoding="utf-8")
                                f.write("{}\n".format(object_dir))
                                f.close()
                else:
                    pass
                count += 1
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
