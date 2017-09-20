"""
"""
from argparse import ArgumentParser
from collections import namedtuple
from json import load
from os import _exit, getcwd
from sys import stderr, stdout

from safgeneration.itemdata import ItemData
from safgeneration.metadata_mapper import MetadataMapperToDublinCore
from safgeneration.simplearchiveformatmaker import SimpleArchiveFormatMaker
from safgeneration.simplearchiveformatvalidator import SimpleArchiveFormatValidator

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
    arguments.add_argument("-", "--output", action='store', type=str,
                           default=getcwd(),
                           help="Optional location to write the SAF directory. default is your working directory")
    parsed = arguments.parse_args()
    try:
        extraction_json = load(open(parsed.extraction_config, 'r', encoding="utf-8"))
        crosswalk_json = load(open(parsed.crosswalk_config, 'r', encoding="utf-8"))
        inventory_lines = _read_lines_from_file(parsed.proquest_inventory)
        safmaker = SimpleArchiveFormatMaker(parsed.output)
        for n_proquest_item in inventory_lines:
            item = ItemData(n_proquest_item, extraction_json)
            mapper = MetadataMapperToDublinCore(crosswalk_json, item.get_metadata())
            metadata = mapper.transform()
            safmaker.add_item(item, metadata)
        safmaker.publish()
        safvalidator = SimpleArchiveFormatValidator(safmaker.get_saf_root(), safmaker.get_total_items())
        safvalidator.validate()
        stdout.write("----\n")
        if not safvalidator.get_validation():
            for error in safvalidator.get_errors():
                stderr.write("{}\n".format(error))
            for error in safmaker.get_errors():
                stderr.write("{}\n".format(error))
            stderr.write("SimpleArchiveFormat directory is not valid\n")
        else:
            stdout.write("SimpleArchiveFormat directory is valid\n")
        stdout.write("----\n")
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
