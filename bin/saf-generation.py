
from argparse import ArgumentParser
import csv
from os import _exit

from safgeneration.utilities import fill_in_saf_directory

def main():
    """the main function of the module
    """
    arguments = ArgumentParser()
    arguments.add_argument("data_location", action="store",
                           type=str,
                           help="Location of the data to create SAFs from",
                          )
    arguments.add_argument("report_file", action="store",
                           type=str,
                           help="The CSV file containing the dissertations " +\
                           "that you want to ingest",
                          )
    parsed = arguments.parse_args()
    with open(parsed.report_file, 'r', encoding="utf-8") as read_file:
        report_reader = csv.reader(read_file, delimiter=",", quotechar="\"")
        count = 0
        relevant_records = []
        for row in report_reader:
            if count > 0:
                a_dict = {}
                title = (row[7])
                first_name = row[4]
                last_name = row[3]
                #a_dict["name"] = "{}, {}".format(last_name, first_name)
                #a_dict["title"] = title
                relevant_records.append(title)
            count += 1
    try:
        fill_in_saf_directory(parsed.data_location, relevant_records)
        #make_archive('SimpleArchiveFormat', 'zip', base_dir=path.join(getcwd(),
        #            'SimpleArchiveFormat'))
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
