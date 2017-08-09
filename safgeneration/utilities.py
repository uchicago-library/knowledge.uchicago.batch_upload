"""a library of functions that bin/saf-generation.py module uses
"""
from collections import namedtuple
from os import getcwd, listdir, mkdir, path, scandir
from shutil import copyfile
from sys import stdout, stderr
from xml.etree import ElementTree as ET

from safgeneration import HARDCODED_VALUES,\
 MAPPER, MULTIPLE_XPATH, SINGLE_XPATH

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
        element.text = text_value.strip()
        return element

def combine_name_parts(name_node):
    """a function to convert a ETree name node into a text string with first, last middle name order
    """
    first = name_node.find("DISS_fname").text
    last = name_node.find("DISS_surname").text
    middle = name_node.find("DISS_middle")
    if middle.text:
        value = last + ", " + first + " " + middle.text
    else:
        value = last + ", " + first
    return value

def extract_an_attribute(a_node, attrib_name):
    """a function to retrieve the binary value from a DISS_binary and return a mimetype "image/pdf"
    """
    return a_node.attrib[attrib_name].lower()

def convert_metadata_to_dublin_core(metadata_package):
    """a function to convert a metadata package object into a dublin core elementtree object
    """
    new_record = build_a_root_element("dublin_core")
    for  key in metadata_package._fields:
        print(key)
        map_info = MAPPER.get(key)
        current_node = getattr(metadata_package, key)
        if key == 'advisor':
            for n_advisor in current_node:
                make_a_new_sub_element(map_info, combine_name_parts(n_advisor), new_record)
        elif key == 'author':
            make_a_new_sub_element(map_info, combine_name_parts(current_node),
                                   new_record)
        elif key == 'subject':
            for n_thing in current_node:
                if n_thing.text:
                    keywords = n_thing.text.split(",")
                    for n_keyword in keywords:
                        make_a_new_sub_element(map_info, n_keyword, new_record)
        elif key == "license":
            if current_node.text == "none" or not current_node.text:
                make_a_new_sub_element(map_info, map_info.get("defaultValue"), new_record)
            else:
                make_a_new_sub_element(map_info, current_node.text, new_record)
        elif key in ['rightsurl', 'publisher']:
            make_a_new_sub_element(map_info, current_node, new_record)
        elif key == "extent":
            make_a_new_sub_element(map_info, extract_an_attribute(current_node, "page_count"),
                                   new_record)
        elif key == "language":
            print(current_node)
            make_a_new_sub_element(map_info, current_node.text + "_US", new_record)
        elif key == "type":
            make_a_new_sub_element(map_info, extract_an_attribute(current_node, "type"), new_record)
        elif key == "mimetype":
            make_a_new_sub_element(map_info, "image/"+extract_an_attribute(current_node, "type"),
                                   new_record)
        elif current_node.text or (current_node.text != 'none'):
            make_a_new_sub_element(map_info, current_node.text, new_record)
    return new_record

def make_a_directory(subdir=None):
    """a function to create a directory in your working directory
    """
    path_to_create = path.join(getcwd(), "SimpleArchiveFormat")
    if subdir:
        path_to_create = path.join(path_to_create, subdir)
    try:
        mkdir(path_to_create)
    except OSError:
        stderr.write("{} already exists.".format(path_to_create))
    return path_to_create

def make_top_saf_directory():
    """a function to create a base SimpleArchiveFormat directory
    """
    return make_a_directory()

def create_saf_directory(identifier):
    """a function to create an item subdirectory in a SimpleArchiveFormat directory
    """
    identifier = 'item_' + identifier
    return make_a_directory(subdir=identifier)

def process_new_input_directory(new_item, item_generator, count):
    """a function to convert a Proquest export into a SimpleArchiveFormat directory
    """
    for n_thing in item_generator:
        if n_thing.name.endswith("DATA.xml"):
            root = get_xml_root(n_thing.path)
            metadata_package = namedtuple("metadata",
                                          "author department copyrightdate issuedate " +\
                                          "degree mimetype extent language license " +\
                                          "title type subject advisor publisher rightsurl")
            counter = 1
            for n_path in SINGLE_XPATH:
                value = find_particular_element(root, n_path[1])
                setattr(metadata_package, n_thing[0], value)
                counter += 1
            for n_path in MULTIPLE_XPATH:
                potential_finds = find_particular_elements(root, n_path[1])
                setattr(metadata_package, n_thing[0], potential_finds[1])
            for n_thing in HARDCODED_VALUES:
                setattr(metadata_package, n_thing[0], n_thing[1])
            new_item.metadata = convert_metadata_to_dublin_core(metadata_package)
        elif n_thing.is_dir():
            attachment_dir = n_thing.path
            new_item.related_items = attachment_dir
        elif n_thing.name.endswith("pdf"):
            major_file = n_thing.path
            new_item.main_file = major_file
    return new_item

def write_contents_file(content_path, root_directory, major_file, related_path=None):
    """a function to write the contents file in a SAF item directory
    """
    related_items_to_copy = []
    with open(content_path, "w") as write_file:
        write_file.write(path.basename("{}\n".format(major_file)))
        if related_path:
            for n_thing in listdir(related_path):
                src_related_filepath = path.join(related_path, n_thing)
                dest_related_filepath = path.join(root_directory,
                                                  path.basename(related_path),
                                                  n_thing)
                related_items_to_copy.append((src_related_filepath, dest_related_filepath))
                write_file.write("{}\n".format(path.join(path.basename(related_path),
                                                         n_thing)))
    return related_items_to_copy

def _find_related_items(a_path):
    """a function to find all related items in a subudirectory and return a list of those paths
    """
    output = []
    print(a_path)
    path_base = path.basename(a_path)
    for n_thing in listdir(a_path):
        output.append(path.join(path_base, n_thing))
    return output

def fill_in_saf_directory(a_location):
    """a function to take a complete SimpleArchiveFormat
    """
    relevant_directories = [scandir(x.path) for x in scandir(a_location)
                            if x.is_dir()]
    all_items = []
    count = 1
    top_saf_directory = ""
    for n_thing in relevant_directories:
        new_item = namedtuple("an_item", "identifier metadata related_items main_file")
        new_item.identifier = str(count).zfill(3)
        new_item = process_new_input_directory(new_item, n_thing, count)
        count += 1
        all_items.append(new_item)
    if all_items:
        top_saf_directory = make_top_saf_directory()
    for n_item in all_items:
        saf_directory = create_saf_directory(n_item.identifier)
        dc_path = path.join(saf_directory, "dublin_core.xml")
        contents_path = path.join(saf_directory, "contents")
        major_file_path = path.join(saf_directory, path.basename(n_item.main_file))
        if not isinstance(n_item.related_items, property):
            related_items = write_contents_file(contents_path, saf_directory,
                                                major_file_path, related_path=n_item.related_items)
        else:
            related_items = write_contents_file(contents_path, saf_directory,
                                                major_file_path)
        copyfile(n_item.main_file, major_file_path)
        ET.ElementTree(n_item.metadata).write(dc_path, encoding='utf-8',
                                              xml_declaration=True)
        if isinstance(n_item.related_items, str):
            related_file_path = path.join(saf_directory, path.basename(n_item.related_items))
            mkdir(related_file_path)
            for n_related_item in related_items:
                copyfile(n_related_item[0], n_related_item[1])
    stdout.write("{} was created\n".format(top_saf_directory))
