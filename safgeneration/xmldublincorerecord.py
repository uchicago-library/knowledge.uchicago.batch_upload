
from xml.etree import ElementTree

class XMLDublinCoreRecord(object):
    def __init__(self, xml_root):
        if isinstance(xml_root, ElementTree.Element) and xml_root.tag == 'dublin_core':
            self._root = xml_root
        else:
            raise ValueError("XMLDublinCoreRecord can only be instantiated with a dublin_core root element")

    def get_field_data(self):
        """a method to return a list of the fields in a xml dublin core record as a list of key:values similar to crosswalk config
        """
        out = []
        for n in self._root:
            a_dict= {"element": n.attrib["element"], "qualifier": n.attrib["qualifier"], "value": n.text}
            out.append(a_dict)
        return out

    def write_out_to_a_file(self, dest_file_path):
        """a method to write the result of the mapping to a file
        """
        tree = ElementTree.ElementTree(self._root)
        tree.write(dest_file_path, xml_declaration=True, encoding="utf-8")

    def __str__(self):
        return ElementTree.tostring(self._root).decode("utf-8")
