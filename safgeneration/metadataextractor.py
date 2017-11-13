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
        print(data_file_path)
        for n_path in self.configuration["singles"]:
            print(n_path)
            if self.configuration["singles"][n_path].get("attribute"):
                element = find_particular_element(root, self.configuration["singles"][n_path]["base"])
                value = element.attrib[self.configuration["singles"][n_path]["attribute"]]
            else:
                value = find_particular_element(root, self.configuration["singles"][n_path]["base"]).text
            if n_path == "copyrightdate":
                m_dict[n_path+'0'] = value.split('/')[2]
            elif n_path == "issuedate":
                m_dict[n_path+'0'] = value.split('/')[2]
            else:
                m_dict[n_path+'0'] = value
        for n_path in self.configuration["multiples"]:
            base_find = find_particular_element(root, self.configuration["multiples"][n_path]["base"])
            rest_find = self.configuration["multiples"][n_path]["tail"]["query"]
            rest_order = self.configuration["multiples"][n_path]["tail"]["display_order"]
            out_strs = []

            if len(rest_find) > 1:
                out_val = []
                if rest_order:
                    ordered_value_list = ['' for x in rest_order]
                for p in rest_find:
                    simple_node = find_particular_element(base_find, p)
                    if n_path == "author" or n_path == "advisor":
                         value = simple_node.text
                         tag_name = simple_node.tag
                         try:
                             rest_order.index(tag_name)
                             ordered_value_list[rest_order.index(tag_name)] = value
                         except ValueError:
                             pass
                    elif value:
                        out_val.append(value.strip())
                if ordered_value_list:
                    new = [x for x in ordered_value_list if x]
                    if len(new) == 3:
                        middle = new[-1]
                        first = new[-2]
                        second_part = first + " " + middle
                        first_part = new[0]
                        val = first_part + ", " + second_part
                    else:
                        val = new[0] + ", " + new[1]
                    out_strs.append(val)
                else:
                    out_strs.append(' '.join(out_val))
            else:
                for p in rest_find:
                    print(p)
                    print(base_find)
                    simple_node = find_particular_elements(base_find, p)
                    print(simple_node)
                    value = []
                    for n in simple_node[1]:
                       value.append(n.text)
                    try:
                        value = ','.join(value)
                    except TypeError:
                        value = None
                    if value and self.configuration["multiples"][n_path]["tail"]["val_type"] == "list":
                        value = value.split(",")
                        count = 0
                        for v in value:
                            m_dict[n_path+str(count)] = v.strip()
                            count += 1
                    elif value and self.configuration["multiples"][n_path]["tail"]["val_type"] == "string":
                        value = value.strip()
                        out_strs.append(value)
            if out_strs:
                m_dict[n_path+'0'] = ' '.join(out_strs)
        if self.configuration.get("hardcoded"):
            for n_option in self.configuration["hardcoded"]:
                m_dict[n_option+'0'] = self.configuration["hardcoded"][n_option]
        return MetadataPackage(m_dict)
