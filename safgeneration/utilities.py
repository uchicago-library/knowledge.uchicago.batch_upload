"""a library of functions that bin/saf-generation.py module uses
"""
from collections import namedtuple
from os import getcwd, listdir, mkdir, path, scandir
from os.path import basename, exists, join, dirname
from shutil import copyfile
from sys import stdout, stderr
from xml.etree import ElementTree as ET
import shutil

def find_files(path):
    """a generator function to retrieve all files in a directory
    """
    for n_item in scandir(path):
        if n_item.is_dir():
            yield from find_files(n_item.path)
        elif n_item.is_file():
            yield n_item.path

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

def extract_an_attribute(a_node, attrib_name):
    """a function to retrieve the binary value from a DISS_binary and return a mimetype "image/pdf"
    """
    return a_node.attrib[attrib_name].lower()

def make_a_directory(new_path):
    """a function to create a directory in your working directory
    """
    if not exists(new_path):
         mkdir(new_path)
