
import re
from .utilities import build_a_root_element, extract_an_attribute,\
                       make_dublincore_element, define_element_attribute,\
                       define_qualifer_element

from .xmldublincorerecord import XMLDublinCoreRecord

class MetadataMapperToDublinCore(object):
    def __init__(self, map_config, data_package):

        self._original = data_package
        self._transform_template = map_config
        required_elements = {}
        for n in map_config:
            required_elements[n] = 0
        self._required_elements = required_elements
        self._errors = []
        self._validation = False

    def validate(self, metadata):
        """a method to check that the result of a transform has all require elements from transform_template
        """
        record_data = metadata.get_field_data()
        for field in record_data:
            element_name_to_seek = field["element"]
            qualifier_to_seek = field["qualifier"]
            search_result = [x[0] for x  in self._transform_template.items()
                            if x[1]['element'] == element_name_to_seek and x[1]['qualifier'] == qualifier_to_seek]
            for key,value in self._transform_template.items():
                try:
                    value['element']
                except KeyError:
                    print((key, value))
            if search_result:
                self._required_elements[search_result[0]] += 1
        check = True
        for key, value in self._required_elements.items():
            if value <= 0:
                self._errors.append("{} field is missing from dublin core metadata record".format(key))
                check &= False
        self._validation = True

    def transform(self):
        root = build_a_root_element("dublin_core")
        for key in self._original.fields:
            field_name = re.split(r'\d{1,}', key)[0]
            map_info = self._transform_template.get(field_name)
            if map_info:
                current_node = getattr(self._original, key)
                new_element = make_dublincore_element(root)
                define_element_attribute(new_element, map_info.get("element"))
                define_qualifer_element(new_element, map_info.get("qualifier"))
                if map_info.get("defaultValue") and current_node == b'none':
                    new_element.text = map_info.get("defaultValue")
                else:
                    new_element.text = current_node.decode()
            else:
                pass
        return XMLDublinCoreRecord(root)

    def get_validation_result(self):
        return self._validation

    def get_errors(self):
        for error in self._errors:
            yield error