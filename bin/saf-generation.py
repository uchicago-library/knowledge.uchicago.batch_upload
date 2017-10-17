"""
"""
from argparse import ArgumentParser
from json import load
from os import _exit, getcwd
from os.path import basename
from sys import stderr, stdout
from xml.etree import ElementTree

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
    arguments.add_argument("-o", "--output", action='store', type=str,
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
            print(item.get_main_file())
            print(n_proquest_item)
            # mapper = MetadataMapperToDublinCore(crosswalk_json, item.get_metadata())
            # metadata = mapper.transform()
            # mapper.validate(metadata)

            # if mapper.get_validation_result() is False:
            #     stderr.write("dublin core metadata created for {} is invalid".format(n_proquest_item))
            #     for error in mapper.get_errors():
            #         stderr.write("{}\n".format(error))
            # else:
            #     stdout.write("dublin core metadata created for {} is valid\n".format(n_proquest_item))
            #     safmaker.add_item(item, metadata)

        # for n in safmaker._items:
        #     print(n.item)
        #     item_title = ElementTree.fromstring(str(n.metadata)).find("dcvalue[@element='title']").text
        #     item_author = ElementTree.fromstring(str(metadata)).find("dcvalue[@element='contributor'][@qualifier='author']").text
        #     print(item_title)
        #     print(item_author)
        #     print(n.item.get_main_file())

        #safmaker.publish()
        #safvalidator = SimpleArchiveFormatValidator(safmaker.get_saf_root(), safmaker.get_total_items())
        #safvalidator.validate()
        #if not safvalidator.get_validation():
        #    for error in safvalidator.get_errors():
        #        stderr.write("{}\n".format(error))
        #    for error in safmaker.get_errors():
        #        stderr.write("{}\n".format(error))
        #    stderr.write("SimpleArchiveFormat directory is not valid\n")
        #else:
        #    stdout.write("SimpleArchiveFormat directory is valid\n")
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
