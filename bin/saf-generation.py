"""
"""
from argparse import ArgumentParser
from collections import namedtuple
from json import load
from os.path import exists, dirname, join, basename, relpath
from os import _exit, scandir, getcwd, mkdir
from shutil import copyfile
from xml.dom import minidom
from xml.etree import ElementTree
from sys import stderr

from safgeneration import MAPPER
from safgeneration.itemdata import ItemData
from safgeneration.metadata_mapper import MetadataMapperToDublinCore

def _make_a_directory(new_path):
    if not exists(new_path):
        mkdir(new_path)
    else:
        stderr.write("{} already exists".format(new_path))

def _read_lines_from_file(file_path):
    lines = []
    with open(file_path, "r", encoding="utf-8") as read_file:
        lines = [x.strip() for x in read_file.readlines()]
    return lines

def main():
    """the main function of the module
    """
    arguments = ArgumentParser()
    arguments.add_argument("proquest_inventory", action="store",
                           type=str,
                           help="Location of the data to create SAFs from",
                          )
    arguments.add_argument("extraction_config", action="store", type=str,
                            help="The config file describing how to get what metadata fields from input metadata")
    arguments.add_argument("crosswalk_config", action='store', type=str,
                           help="The config file describing what to map input metadata fields to what element for output metadata")
    parsed = arguments.parse_args()
    try:
        extraction_json = load(open(parsed.extraction_config, 'r', encoding="utf-8"))
        crosswalk_json = load(open(parsed.crosswalk_config, 'r', encoding="utf-8"))
        total = 1
        inventory_lines = _read_lines_from_file(parsed.proquest_inventory)
        _make_a_directory(join(getcwd(), 'SimpleArchiveFormat'))
        for n_proquest_item in inventory_lines:
            item = ItemData(n_proquest_item, extraction_json)
            metadata = MetadataMapperToDublinCore(crosswalk_json, item.metadata)
            print(metadata)
            # base_path = join(getcwd(), 'SimpleArchiveFormat', 'item_' + str(total).zfill(3))
            # _make_a_directory(base_path)
            # dc_file_path = join(base_path, "dublin_core.xml")
            # contents_file_path = join(base_path, "contents")
            # new_item.write_metadata_to_a_file(dc_file_path)
            # new_item.copy_main_file_to(base_path)
            # new_item.copy_related_items(base_path)
            # item_contents = [relpath(x, base_path) for x in find_files(base_path) if not x.endswith(".xml")]
            # with open(contents_file_path, "w+", encoding="utf-8") as write_file:
            #     for n_item in item_contents:
            #         write_file.write("{}\n".format(n_item))
            # if not item_contents:
            #     print("{} did not have contents copied to {}".format(n_proquest_item, base_path))
            # total += 1
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
