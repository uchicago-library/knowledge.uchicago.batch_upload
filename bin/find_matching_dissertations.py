"""
"""
from argparse import ArgumentParser
import csv
from os.path import dirname, getcwd, join
from os import _exit

from safgeneration.utilities import fill_in_saf_directory, find_particular_element, find_files, get_xml_root

SINGLE_XPATH = [
    ("author", "DISS_authorship/DISS_author[@type='primary']/DISS_name"),
    ("department", "DISS_description/DISS_institution/DISS_inst_contact"),
    ("copyrightdate", "DISS_description/DISS_dates/DISS_accept_date"),
    ("issuedate", "DISS_description/DISS_dates/DISS_accept_date"),
    ("degree", "DISS_description/DISS_degree"),
    ("mimetype", "DISS_content/DISS_binary"),
    ("extent", "DISS_description"),
    ("language", "DISS_description/DISS_categorization/DISS_language"),
    ("license", "DISS_creative_commons_license/DISS_abbreviation"),
    ("title", "DISS_description/DISS_title"),
    ("type", "DISS_description")
]

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
    arguments.add_argument("-o", "--output", help="File to write out output", action='store',
                           type=str, default=join(getcwd(), "matches.txt"))
    parsed = arguments.parse_args()
    with open(parsed.report_file, 'r', encoding="utf-8") as read_file:
        report_reader = csv.reader(read_file, delimiter=",", quotechar="\"")
        count = 0
        relevant_records = []
        for row in report_reader:
            if count > 0:
                title = row[6].encode("utf-8")
                relevant_records.append(title)
            count += 1
    try:
        actual_count = count - 1
        gen = _find_files(parsed.data_location)
        matches = 0
        a_list = []
        for n_item in gen:
            if n_item.endswith("_DATA.xml"):
                if matches < actual_count:
                    root = get_xml_root(n_item)
                    for n_option in SINGLE_XPATH:
                        if n_option[0] == 'title':
                            check = find_particular_element(root, "DISS_description/DISS_title")
                            check = check.text.encode("utf-8")
                            filtered = [x for x in relevant_records if x == check]
                            if filtered:
                                matches += 1
                                write_file = open("data/matched_proquest_dirs.txt", "a+", encoding="utf-8")
                                write_file.write("{}\n".format(dirname(n_item)))
                                write_file.close()
                else:
                    break
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
