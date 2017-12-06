"""a module to take a list of DOIS and modify the redirect locations

"""
from argparse import ArgumentParser
from os import _exit
from sys import stderr, stdout
import requests
from rccingest.RecordReader import RecordReader
from rccingest.EZIDActor import EZIDActor

def main():
    arguments = ArgumentParser(description="A tool to take a list of DOIs and modify the target URI programmatically")
    arguments.add_argument("spreadsheet", type=str, action='store',
                           help="A CSV file containing the DOIs " +
                           "that need to be changed and the " +
                           "new locations that need to be added to those DOIs")
    parsed = arguments.parse_args()
    try:
        data = RecordReader(parsed.spreadsheet)
        username = input("Enter your EZID username:")
        password = input("Enter your EZID password:")
        while data.get_records_left() > 0:
            cur = data.get_an_item()
            doi, loc = cur
            actor = EZIDActor()
            test_loc_url = requests.get(loc)
            if test_loc_url.status == 200:
                posting = actor.post_data(doi, loc, username, password)
            else:
                posting = 'null'
            if posting == 'null':
                stderr.write("Could not set the new target for the DOI {}\n".format(doi))
            else:
                stdout.write("{} has been changed to redirect to {}\n".format(doi, loc))
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
