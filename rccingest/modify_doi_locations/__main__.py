"""a module to take a list of DOIS and modify the redirect locations

"""
from argparse import ArgumentParser
import csv
from getpass import getpass
from os.path import join
from os import _exit, getcwd
import requests
from sys import stderr, stdout

from rccingest.RecordReader import RecordReader
from rccingest.EZIDActor import EZIDActor
from rccingest.KnowledgeAPIActor import KnowledgeAPIActor

def main():
    arguments = ArgumentParser(description="A tool to take a list of DOIs and modify the target URI programmatically")
    arguments.add_argument("spreadsheet", type=str, action='store',
                           help="A CSV file containing the DOIs " +
                           "that need to be changed and the " +
                           "new locations that need to be added to those DOIs")
    arguments.add_argument("-o", "--output", action='store', type=str,
                           
                           help="Where to write the CSV file to batch edit the metadata in knowledge.uchicago.edu",
                           default=join(getcwd(), 'knowledge_uchicago_batch_metadata_edits.csv'))
    parsed = arguments.parse_args()
    try:
        data = RecordReader(parsed.spreadsheet)
        username = input("Enter your EZID username:")
        password = getpass()
        record_rows = []
        while data.get_records_left() > 0:
            cur = data.get_an_item()
            doi, title, loc = cur
            actor = EZIDActor()
            test_loc_url = requests.get(loc, verify=False)
            if test_loc_url.status_code == 200:
                posting = actor.post_data(doi, loc, username, password)
            else:
                posting = 'null'
            if posting == 'null':
                stderr.write("Could not set the new target for the DOI {}\n".format(doi))
            else:
                stdout.write("{} has been changed to redirect to {}\n".format(doi, loc))
            dspace_actor = KnowledgeAPIActor()
            request_data = dspace_actor.search_for_an_item_by_title(title)
            if request_data:
                knowledge_record_id = request_data[0]['id']
                record_row = [knowledge_record_id, title, "https://doi.org/"+doi]
                record_rows.append(record_row)
        with open(parsed.output, "w+", encoding="utf-8") as write_file:
            writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["id", "title", "dc.identifier.uri"])
            for row in record_rows:
                writer.writerow(row)
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
