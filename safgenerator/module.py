
from argparse import ArgumentParser
from collections import namedtuple
from csv import reader
from os import _exit, scandir
from xml.etree import ElementTree as ET

DEFAULT_RIGHTS = "University of Chicago dissertations are covered by copyright." +\
                 " They may be viewed from this source for any purpose," +\
                 "but reproduction or distribution in any format is " +\
                 "prohibited without written permission."

SINGLE_XPATH = [
    ("firstname", "DISS_authorship/DISS_author[@type='primary']/" +\
    "DISS_name/DISS_fname"),
    ("middlename", "DISS_authorship/DISS_author[@type='primary']/" +\
    "DISS_name/DISS_middle"),
    ("lastname", "DISS_authorship/DISS_author[@type='primary']/" +\
    "DISS_name/DISS_surname"),
    ("department", "DISS_description/DISS_institution/" +\
    "DISS_inst_contact"),
    ("orcid", "DISS_authorship/DISS_author/" +
     "DISS_orcid"),
    ("copyrightdate", "DISS_description/DISS_dates/" +
     "DISS_accept_date"),
    ("degree", "DISS_content/DISS_abstract/DISS_para",
     "DISS_description/DISS_degree"),
    ("mimetype", "DISS_content/DISS_binary"),
    ("the_license", "DISS_creative_commons_license/DISS_abbreviation"),
    ("title", "DISS_description/DISS_title"),
    ("processingcode", "DISS_description/DISS_institution/" +
     "DISS_processing_code"),
    ("delayed_release", "DISS_repository/DISS_delayed_release")
]

MULTIPLE_XPATH = [
    ("attachments", "DISS_content/DISS_attachment/DISS_file_name"),
    ("subjects", "DISS_description/DISS_categorization/DISS_keyword"),
    ("advisors", "DISS_description/DISS_advisor/DISS_name"),
]

MAP = {
    "firstname":{"element":"contributor", "qualifier":"author", "pos":0},
    "middlename":{"element":"contributor", "qualifier":"author", "pos":0},
    "lastname":{"element":"contributor", "qualifier":"author", "pos":0},

    "department":{"element":"contributor", "qualifier":"author", "pos":0},
    "orcid":{"element":"contributor", "qualifier":"author", "pos":0},
    "copyrightdate":{"element":"contributor", "qualifier":"author", "pos":0},
    "degree":{"element":"contributor", "qualifier":"author", "pos":0},
    "mimetype":{"element":"format", "qualifier":"mimetype", "pos":0},

    "the_license":{"element":"contributor", "qualifier":"author", "pos":0},
    "title":{"element":"contributor", "qualifier":"author", "pos":0},
    "processingcode":{"element":"contributor", "qualifier":"author", "pos":0},
    "delayed_release":{"element":"contributor", "qualifier":"author", "pos":0},
    "abstract":{"element":"description", "qualifier":"none", "pos":0},
    "subjects":{"element": "subject", "qualifier": "none", "pos": 0},
    "advisors":{"element": "contributor", "qualifier": "advisor", "pos": 0}
}

def make_dublincore_element(root):
    """a function to make a dublin core elementtree object
    """
    return ET.SubElement(root, 'dcvalue')

def define_attribute_value(an_element, attribute_name, attribute_value):
    """an element to add an attribute to an elementtree element object
    """
    return an_element.set(attribute_name, attribute_value)

def default_qualifier_attribute(an_element):
    """set attribute qualifier with value none on an elementtree object
    """
    return define_attribute_value(an_element, "qualifier", "none")

def define_element_attribute(an_element, element_name):
    """set attribute element with defined value on an elementtree object
    """
    return define_attribute_value(an_element, "element", element_name)

def define_qualifer_element(an_element, qualifier_value):
    """set attribute qualifier with defined value on an elementtree object
    """
    return define_attribute_value(an_element, "qualifier", qualifier_value)

def get_xml_root(xml_path):
    """a function to get an xml root from a path to an xml file
    """
    xml_doc = ET.parse(xml_path)
    xml_root = xml_doc.getroot()
    return xml_root

def find_particular_element(root, xpath_path):
    """a function to search for a particular XPath path in an xml root
    """
    searching = root.find(xpath_path)
    if searching:
        return (True, searching)
    else:
        return (False,)

def find_particular_elements(root, xpath_path):
    """a function to search for all instances of a particular XPath path in an xml root
    """
    searching = root.findall(xpath_path)
    if searching:
        return (True, searching)
    else:
        return (False,)

def build_and_populate_dublin_core(metadata_package):
    new_root = ET.Element("dublin_core")


def main():
    """the main function of the module
    """
    arguments = ArgumentParser()
    arguments.add_argument("index_file", action='store', type='str',
                           help="Location of index file")
    arguments.add_argument("data location", action="store", type="str",
                           help="Location of the data to create SAFs from")
    parsed = arguments.parse_args()
    index_data = reader(open(parsed.index_file, "rb"))
    relevant_directories = [scandir(x.path) for x in scandir(parsed.data_location)
                            if x.is_dir()]
    all_items = []
    count = 1
    for n_thing in relevant_directories:
        new_item = namedtuple("an_item", "identifier metadata related_items main_file")
        new_item.identifier = str(count).zfill(3)
        if n_thing.name.endswith("DATA.xml"):
            root = get_xml_root(n_thing.path)

            metadata_package = namedtuple("metadata",
                                          "advisors first_name middle_name last_name " +
                                          "department orcid copyright_date abstract_paragraphs " +
                                          "degree mimetype the_license rights subjects " +
                                          "processing_code delayed_release attachments")
            for n_thing in SINGLE_XPATH:
                setattr(metadata_package, n_thing[0], find_particular_element(root, n_thing[1]))
            for n_thing in MULTIPLE_XPATH:
                setattr(metadata_package, n_thing[0], find_particular_element(root, n_thing[1]))
            new_item.metadata = metadata_package
        elif n_thing.is_dir():
            attachment_dir = n_thing.path
            new_item.related_items = attachment_dir
        elif n_thing.name.endswith("pdf"):
            major_file = n_thing.path
            new_item.main_file = major_file
        all_items.append(new_item)
        count += 1

if __name__ == "__main__":
    _exit(main())
