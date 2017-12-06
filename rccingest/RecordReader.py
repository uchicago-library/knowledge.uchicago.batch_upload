"""class definition for record reader
"""
from os.path import exists
import csv

class RecordReader(object):
    """a class to read data from spredsheet and to verify that each record is correct
    """
    def __init__(self, a_file_path):
        if not exists(a_file_path):
            raise ValueError("You must input a CSV file that actually exists.")
        else:
            self.csv_file = a_file_path
            self.csv_records = self._parse_file()
            self.num_records = len(self.csv_records)

    def _parse_file(self):
        headers = []
        first_out = []
        second_out = []
        with open(self.csv_file, "r", encoding="utf-8") as read_file:
            csv_reader = csv.reader(read_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            for record in csv_reader:
                first_out.append(record)
        headers = first_out[0]
        for row in first_out[1:]:
            a_dict = {}
            for header in headers:
                a_dict[header] = row[headers.index(header)]
            second_out.append(a_dict)
        valid_header_fields = ["doi", "new_location"]
        difference = list(set(valid_header_fields) - set(headers))
        if len(difference) > 0:
            raise ValueError("You must include a DOI field and a new_location")
        else:
            return second_out

    def get_records_left(self): 
        """a method to return the number of records in the list
        """
        return self.num_records

    def get_an_item(self):
        """a method to get the next item in the records

        if there are no more records left returns NoneType
        """
        records_left = len(self.csv_records)
        if records_left > 0:
            self.num_records = records_left - 1
            popped = self.csv_records.pop()
            return (popped["doi"], popped["new_location"])
        else:
            return None
       

    def find_an_item_by_doi(self, doi_string):
        """a method to find a particular record by title

        if there are no matching records returns NoneType
        """
        if self.csv_records:
            for a_record in self.csv_records:
                if a_record.get("doi") == doi_string:
                    
                    return (a_record["doi"], a_record["new_location"])
        return None

    def validate(self):
        """a method to inform the user of the first invalid record in the spreadsheet
        """
        count = 1
        message = ""
        for record in self.csv_records:
            doi = record.get("doi", None)
            loc = record.get("new_location", None)
            if not doi:
                message += "Record number {} is missing DOI that needs to be changed\n"
                raise ValueError("Record ")
            if not loc:
                message += "Record number {} is missing new location\n"
            count += 1
        if message != "":
            raise ValueError(message)
        else:
            return True