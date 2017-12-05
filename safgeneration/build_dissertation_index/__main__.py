"""command-line script to find the mamluk CHOs that you care about right now
"""
from argparse import ArgumentParser
import csv
from os import getcwd, scandir
from os.path import basename, join, split, normpath
from os import _exit
from sys import stdout
from xml.etree import ElementTree

    #     "author": {"base": "DISS_authorship/DISS_author[@type='primary']/DISS_name",
    #                 "tail": {"query": ["DISS_fname", "DISS_middle", "DISS_surname"],
	#  	    	     "display_order": ["DISS_surname", "DISS_fname", "DISS_middle"],
    #                          "val_type": "string"
    #                         }
    #               }
    # },
    # "title": {"base": "DISS_description/DISS_title"},

def splitpath(path):
    parts = []
    path, tail = split(path)
    while path and tail:
        parts.append(tail)
        path, tail = split(path)
    parts.append(join(path, tail))
    parts.reverse()
    return [normpath(x) for x in parts]

def _find_proquest_objects(path, index_location, root):
    for n_item in scandir(path):
        if n_item.is_dir():
            yield from _find_proquest_objects(n_item.path, index_location, root)
        elif n_item.is_file and n_item.path.endswith("_DATA.xml"):
            xml_root = ElementTree.parse(n_item.path).getroot()
            pot_title = xml_root.find("DISS_description/DISS_title").text
            pot_author = xml_root.find("DISS_authorship/DISS_author[@type='primary']/DISS_name")
            pot_first_name = pot_author.find("DISS_fname").text
            pot_last_name = pot_author.find("DISS_surname").text
            found = False
            reader = csv.reader(open(index_location, "r", encoding="utf-8"),
                                     quoting=csv.QUOTE_ALL, delimiter=',', quotechar='"')
            for row in reader:
                length_of_row = len(row)
                if length_of_row == 4:
                    if row[-1] == "\"" + n_item.path + "\"":
                        found = True
                        break
            if not found:
                split_filepath = n_item.path.split(root)[1]
                print(split_filepath)
                yield [pot_title, pot_first_name, pot_last_name, split_filepath]

def main():
    """the main function of the module
    """
    arguments = ArgumentParser()
    arguments.add_argument("data_location",
                           help="Location of the dissertation ProQuest data",
                           action="store", type=str)
    arguments.add_argument("index_location",
                           help="Location of the dissertation index file",
                           action="store", type=str)
    arguments.add_argument("root",
                           help="Location of the dissertation index file",
                           action="store", type=str, default="Z:/Dissertation Offices/")
    parsed = arguments.parse_args()
    try:
        generator = _find_proquest_objects(parsed.data_location, parsed.index_location, parsed.root)
        with open(parsed.index_location, "a+", encoding="utf-8") as write_file:
            writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["title, last_name", "first_name", "file_path"])
            for record in generator:
                print(record)
                writer.writerow(record)
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
