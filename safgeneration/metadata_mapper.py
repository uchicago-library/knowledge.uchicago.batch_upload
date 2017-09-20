
import re
from .utilities import build_a_root_element, extract_an_attribute,\
                       make_dublincore_element, define_element_attribute,\
                       define_qualifer_element

from .xmldublincorerecord import XMLDublinCoreRecord

class MetadataMapperToDublinCore(object):
    def __init__(self, map_config, data_package):

        self._original = data_package
        self._transform_template = map_config

    def transform(self):
        root = build_a_root_element("dublin_core")
        for key in self._original.fields:
            field_name = re.split(r'\d{1,}', key)[0]
            map_info = self._transform_template.get(field_name)
            current_node = getattr(self._original, key)
            new_element = make_dublincore_element(root)
            define_element_attribute(new_element, map_info.get("element"))
            define_qualifer_element(new_element, map_info.get("qualifier"))
            if map_info.get("defaultValue") and current_node == b'none':
                new_element.text = map_info.get("defaultValue")
            else:
                new_element.text = current_node.decode()
        return XMLDublinCoreRecord(root)

