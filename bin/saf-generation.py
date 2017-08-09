
from argparse import ArgumentParser

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
    try:
        fill_in_saf_directory(parsed.data_location)
        #make_archive('SimpleArchiveFormat', 'zip', base_dir=path.join(getcwd(),
        #            'SimpleArchiveFormat'))
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
