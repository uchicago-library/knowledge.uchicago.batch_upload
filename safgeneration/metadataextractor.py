"""
"""
from .utilities import get_xml_root, find_particular_element, find_particular_elements

class MetadataPackage(object):
    def __init__(self, a_dict):
        self.fields = a_dict.keys()
        for n_key in a_dict.keys():
            setattr(self, n_key, str(a_dict[n_key]).encode("utf-8"))

class MetadataExtractor(object):
    def __init__(self, extraction_conf):
        self.configuration = extraction_conf

    def create(self, data_file_path):
        m_dict = {}
        root = get_xml_root(data_file_path)
        for n_path in self.configuration["singles"]:
            if self.configuration["singles"][n_path].get("attribute"):
                element = find_particular_element(root, self.configuration["singles"][n_path]["base"])
                value = element.attrib[self.configuration["singles"][n_path]["attribute"]]
            else:
                value = find_particular_element(root, self.configuration["singles"][n_path]["base"]).text
            m_dict[n_path+'0'] = value
        for n_path in self.configuration["multiples"]:
            base_find = find_particular_element(root, self.configuration["multiples"][n_path]["base"])
            rest_find = self.configuration["multiples"][n_path]["tail"]["query"]
            out_strs = []
            if len(rest_find) > 1:
                out_val = []
                for p in rest_find:
                    simple_node = (find_particular_element(base_find, p))
                    value = simple_node.text
                    if value:
                        out_val.append(value.strip())
                out_strs.append(' '.join(out_val))
            else:
                for p in rest_find:
                    simple_node = (find_particular_element(base_find, p))
                    value = simple_node.text
                    if value and self.configuration["multiples"][n_path]["tail"]["val_type"] == "list":
                        value = value.split(",")
                        count = 0
                        for v in value:
                            m_dict[n_path+str(count)] = v
                            count += 1
                    elif value and self.configuration["multiples"][n_path]["tail"]["val_type"] == "string":
                        value = value
                        out_strs.append(value)
            if out_strs:
                m_dict[n_path+'0'] = ' '.join(out_strs)
        for n_option in self.configuration["hardcoded"]:
            m_dict[n_option+'0'] = self.configuration["hardcoded"][n_option]
        return MetadataPackage(m_dict)
