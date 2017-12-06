from argparse import ArgumentParser
from os import _exit, mkdir
from os.path import join
import csv
import json
from sys import stderr
from safgeneration.metadata_mapper import MetadataMapperToDublinCore
from safgeneration.metadataextractor import MetadataPackage

def main():
    arguments = ArgumentParser(description="A tool to take a spreadsheet of metadata and generate a SimpleArchiveFormat directory with no binary files")
    arguments.add_argument("spreadsheet", type=str, action='store',
                           help="A CSV file containing a row for each item that you want to create with the metadta fields that you want to put in the dublin core XML file for each item")
    arguments.add_argument("crosswalk", type=str, action='store',
                           help="A configuration for how to crosswalk")
    parsed = arguments.parse_args()
    try:
        crosswalk_json = json.load(open(parsed.crosswalk, 'r', encoding="utf-8"))
        with open(parsed.spreadsheet, "r", encoding="utf-8") as read_file:
            reader = csv.DictReader(read_file, delimiter=',',
                                    fieldnames = ['title', 'author_fname', 'author_lname', 'publisher', 'description', 'rights statement', 'rights url'],
                                    quotechar='"', quoting=csv.QUOTE_ALL)
            count = 1
            in_data = []
            mkdir("./SimpleArchiveFormat")
            for row in reader:
                if count == 0 and row['title'] == 'title':
                    pass
                else:
                    in_data.append(row)
                count += 1
            item_count = 1
            for record in in_data:
                record["author"] = record["author_lname"] + ", " + record["author_fname"]
                mdata_pkg = MetadataPackage(record)
                mapper = MetadataMapperToDublinCore(crosswalk_json, mdata_pkg)
                metadata = mapper.transform()
                item_dir = join("./SimpleArchiveFormat",
                                "item_" + str(item_count).zfill(3))
                mkdir(item_dir)
                contents_filepath = join(item_dir, "contents")
                contents_filepath = open(contents_filepath, "w+", encoding="utf-8")
                contents_filepath.close()
                mdata_file_path = join(item_dir, "dublin_core.xml")
                metadata.write_out_to_a_file(mdata_file_path)
                item_count += 1
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
