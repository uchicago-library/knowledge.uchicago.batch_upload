
from argparse import ArgumentParser
from collections import namedtuple
from os import _exit, getcwd, listdir, path, mkdir, scandir
from shutil import copyfile
from sys import stderr
from xml.etree import ElementTree as ET

DEFAULT_RIGHTS = "University of Chicago dissertations are covered by copyright." +\
                 " They may be viewed from this source for any purpose," +\
                 "but reproduction or distribution in any format is " +\
                 "prohibited without written permission."


SINGLE_XPATH = [
    ("author", "DISS_authorship/DISS_author[@type='primary']/DISS_name"),
    ("department", "DISS_description/DISS_institution/DISS_inst_contact"),
    ("copyrightdate", "DISS_description/DISS_dates/DISS_accept_date"),
    ("issuedate", "DISS_description/DISS_dates/DISS_accept_date"),
    ("degree", "DISS_description/DISS_degree"),
    ("mimetype", "DISS_content/DISS_binary"),
    ("license", "DISS_creative_commons_license/DISS_abbreviation"),
    ("title", "DISS_description/DISS_title"),
]

MULTIPLE_XPATH = [
    ("subject", "DISS_description/DISS_categorization/DISS_keyword"),
    ("advisor", "DISS_description/DISS_advisor/DISS_name"),
]

MAPPER = {
    "advisor": {"element":"contrbutor", "qualifier":"advisor"},
    "author": {"element":"contributor", "qualifier":"author"},
    "department": {"element": "contributor", "qualifier":"department"},
    "copyrightdate": {"element": "date", "qualifier": "copyright"},
    "issuedate": {"element": "date", "qualifier": "issued"},
    "abstract": {"element": "description", "qualifier": "none"},
    "degree": {"element": "description", "qualifier": "degree"},
    "mimetype": {"element": "format", "qualifier": "mimetype"},
    "extent": {"element": "format", "qualifier": "extent"},
    "language": {"element": "language", "qualifier": "iso"},
    "publisher": {"element": "publisher", "qualifier": "none"},
    "license": {"element": "rights", "qualifier": "none",
                "defaultValue": DEFAULT_RIGHTS},
    #{"element": "rights", "qualifier": "uri"},
    "subject": {"element": "subject", "qualifier": "none"},
    "title": {"element": "title", "qualifier": "none"},
    "type": {"element": "type", "qualifier": "none"}
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
    return searching

def find_particular_elements(root, xpath_path):
    """a function to search for all instances of a particular XPath path in an xml root
    """
    searching = root.findall(xpath_path)
    if searching:
        return (True, searching)
    else:
        return (False,)

def build_a_root_element(element_name):
    """a function to return a root dublin core element
    """
    return ET.Element(element_name)

def make_a_new_sub_element(map_data, text_value, current_record):
    """a function to create a new subelement of a dublin core root
    """
    element = make_dublincore_element(current_record)
    if isinstance(map_data, list):
        pass
    else:
        define_element_attribute(element, map_data.get("element"))
        define_qualifer_element(element, map_data.get("qualifier"))
        element.text = text_value
        return element

def deal_with_combinationValue_mapping(new_value, element_map_data, current_record):
    """a function to update the required element in a combinationValue mapping with the new data
    """
    xpath = element_map_data.get("element") + "[@qualifier=\"" +\
            element_map_data.get("qualifier") + "\"]"
    element_already_there = current_record.find(xpath)
    if element_already_there:
        current_value = element_already_there.text
        new_value_position = element_map_data.get("position")
        listifed = current_value.split(" ")
        listifed.insert(new_value_position, new_value)
        new_value = " ".join(listifed)
    else:
        new_value = new_value
    element = make_a_new_sub_element(element_map_data, new_value, current_record)
    return element

def convert_metadata_to_dublin_core(metadata_package):
    """a function to convert a metadata package object into a dublin core elementtree object
    """
    new_record = build_a_root_element("dublin_core")
    for  key in metadata_package._fields:
        map_info = MAPPER.get(key)
        if key in ['advisor']:
            list = getattr(metadata_package, key)
            for n in list:
                value = n
                first = value.find("DISS_fname").text
                last = value.find("DISS_surname").text
                middle = value.find("DISS_middle")
                if middle.text:
                    value =  last + ", " + first + " " + middle.text
                else:
                    value =  last + ", " + first
                make_a_new_sub_element(map_info, value, new_record)
        elif key in ['author']:
            value = getattr(metadata_package, key)
            first = value.find("DISS_fname").text
            last = value.find("DISS_surname").text
            middle = value.find("DISS_middle")
            if middle.text:
                value =  last + ", " + first + " " + middle.text
            else:
                value =  last + ", " + first
            make_a_new_sub_element(map_info, value, new_record)
        elif key in ['subject']:
            list = getattr(metadata_package, key)
            for n in list:
                if n.text:
                    keywords = n.text.split(",")
                    for n in keywords:
                        make_a_new_sub_element(map_info, n, new_record)
        else:
            value = getattr(metadata_package, key)
            if value.tag == "DISS_binary":
                new = "image/" + value.attrib["type"].lower()
                make_a_new_sub_element(map_info, new, new_record)
            if value.text or (value.text != none):
                make_a_new_sub_element(map_info, value.text, new_record)
    return new_record

def make_top_saf_directory():
    path_to_top_directory = path.join(getcwd(), 'SimpleArchiveFormat')
    try:
        mkdir(path_to_top_directory)
    except OSError:
        stderr.write("SimpleArchiveFormat already exists in your working directory\n")
    return path_to_top_directory

def create_saf_directory(identifier):
    identifier = 'item_' + identifier
    path_to_a_saf = path.join(getcwd(), 'SimpleArchiveFormat', identifier)
    try:
        mkdir(path_to_a_saf)
    except OSError:
        stderr.write("SimpleArchiveFormat/{} already exists in your working directory\n".format(identifier))
    return path_to_a_saf

def process_new_input_directory(new_item, item_generator, count):
    for n_thing in item_generator:
        if n_thing.name.endswith("DATA.xml"):
            root = get_xml_root(n_thing.path)
            metadata_package = namedtuple("metadata", "author department copyrightdate issuedate degree mimetype license" +\
                                          " title subject advisor")
            counter = 1
            for n_thing in SINGLE_XPATH:
                label = n_thing[0]
                setattr(metadata_package, label, find_particular_element(root, n_thing[1]))
                counter += 1
            for n_thing in MULTIPLE_XPATH:
                label = n_thing[0]
                count = 1
                potential_finds = find_particular_elements(root, n_thing[1])
                setattr(metadata_package, n_thing[0], potential_finds[1])
            new_item.metadata = convert_metadata_to_dublin_core(metadata_package)
        elif n_thing.is_dir():
            attachment_dir = n_thing.path
            new_item.related_items = attachment_dir
            print(new_item.related_items)
        elif n_thing.name.endswith("pdf"):
            major_file = n_thing.path
            new_item.main_file = major_file
    return new_item

def main():
    """the main function of the module
    """
    arguments = ArgumentParser()
    arguments.add_argument("data_location", action="store", type=str,
                           help="Location of the data to create SAFs from")
    parsed = arguments.parse_args()
    relevant_directories = [scandir(x.path) for x in scandir(parsed.data_location)
                            if x.is_dir()]
    all_items = []
    count = 1
    for n_thing in relevant_directories:
        new_item = namedtuple("an_item", "identifier metadata related_items main_file")
        new_item.identifier = str(count).zfill(3)
        new_item = process_new_input_directory(new_item, n_thing, count)
        count += 1
        all_items.append(new_item)
    if len(all_items) > 0:
        make_top_saf_directory()
    for n_item in all_items:
        saf_directory = create_saf_directory(n_item.identifier)
        dc_path = path.join(saf_directory, "dublin_core")
        contents_path = path.join(saf_directory, "contents")
        major_file_path = path.join(saf_directory, path.basename(n_item.main_file))
        if isinstance(n_item.related_items, str):
            related_file_path = path.join(saf_directory, path.basename(n_item.related_items))
            mkdir(related_file_path)
        else:
            related_file_path = None
        copyfile(n_item.main_file, major_file_path)
        ET.ElementTree(n_item.metadata).write(dc_path, encoding='utf-8', xml_declaration=True)
        related_items_to_copy = []
        with open(contents_path, "w") as write_file:
            write_file.write(path.basename("{}\n".format(n_item.main_file)))
            if related_file_path:
                for n_thing in listdir(n_item.related_items):
                    src_related_filepath = path.join(n_item.related_items, n_thing)
                    dest_related_filepath = path.join(saf_directory,
                                                      path.basename(n_item.related_items),
                                                      n_thing)
                    related_items_to_copy.append((src_related_filepath, dest_related_filepath))
                    write_file.write("{}\n".format(path.join(path.basename(n_item.related_items), n_thing)))
        for n_related_item in related_items_to_copy:
            copyfile(n_related_item[0], n_related_item[1])
    return 0

if __name__ == "__main__":
    _exit(main())
