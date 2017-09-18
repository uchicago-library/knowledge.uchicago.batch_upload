
from argparse import ArgumentParser
from collections import namedtuple
import csv
from os.path import abspath, exists, dirname, join, basename
from os import _exit, scandir, getcwd, mkdir
from shutil import copyfile
from xml.dom import minidom
from xml.etree import ElementTree
from sys import stderr

from safgeneration.utilities import process_new_input_directory

def main():
    """the main function of the module
    """
    arguments = ArgumentParser()
    arguments.add_argument("proquest_inventory", action="store",
                           type=str,
                           help="Location of the data to create SAFs from",
                          )
    parsed = arguments.parse_args()

    try:
        inventory_lines = []
        with open(parsed.proquest_inventory, "r", encoding="utf-8") as read_file:
            inventory_lines = [x.strip() for x in read_file.readlines()]

        total = 1
        if not exists(join(getcwd(), 'SimpleArchiveFormat')):
            mkdir(join(getcwd(), 'SimpleArchiveFormat'))
        for n_proquest_item in inventory_lines:
            new_item = namedtuple("an_item", "identifier metadata related_items main_file")
            new_item = process_new_input_directory(new_item, scandir(n_proquest_item), total)
            base_path = join(getcwd(), 'SimpleArchiveFormat', 'item_' + str(total).zfill(3))
            if not exists(base_path):
                mkdir(base_path)
            contents_file_path = join(base_path, "contents")
            dc_file_path = join(base_path, "dublin_core.xml")
            dc_data = minidom.parseString(ElementTree.tostring(new_item.metadata))
            with open(dc_file_path, 'w+', encoding="utf-8") as write_file:
                dc_data.writexml(write_file, encoding="utf-8")
            if not exists(dc_file_path):
                with open(dc_file_path, "w", encoding="utf-8") as write_file:
                    write_file.write(dc_data)
            if not exists(join(base_path, basename(new_item.main_file))):
                try:
                    copyfile(new_item.main_file, join(base_path, basename(new_item.main_file)))
                except OSError:
                    print("{} couldn't be copied\n".format(new_item.main_file))
            contents_data = []
            contents_data.append(basename(new_item.main_file))

            total += 1
            if not isinstance(new_item.related_items, property):

                rel_item_base_path = join(base_path, basename(new_item.related_items))
                if not exists(rel_item_base_path):
                    mkdir(rel_item_base_path)
                for n in scandir(new_item.related_items):
                    src = n.path
                    dest = join(rel_item_base_path, basename(n.path))
                    contents_data.append(join(basename(dirname(src)), basename(src)))
                    if not exists(dest):
                        try:
                            copyfile(src, dest)
                        except OSError:
                            print("{} couldn't be copied.\n".format(src))
            with open(join(base_path, 'contents'), 'w+', encoding="utf-8") as write_file:
                for p in contents_data:
                    new = p.translate(str.maketrans("\\", "/"))
                    print(new)
                    write_file.write("{}\n".format(new))

        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
