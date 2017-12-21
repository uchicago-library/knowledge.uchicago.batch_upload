from xml.etree import ElementTree as ET
from os import scandir
from os.path import basename, dirname, exists, join
import shutil
from sys import stderr

from .metadatapackageextractorbuilder import MetadataPackageExtractorBuilder
from .utilities import find_particular_element, find_particular_elements, get_xml_root, make_a_directory

class ItemData(object):
    def __init__(self, a_directory, extraction_config):
        self.root  = a_directory
        an_etd_directory = [x for x in scandir(a_directory)]
        data_file = [x for x in an_etd_directory if x.path.endswith("DATA.xml")]
        pdf_file = [x for x in an_etd_directory if x.path.endswith(".pdf")]
        related_items_dir = [x for x in an_etd_directory if x.is_dir()]
        if related_items_dir:
            self._related_items = [x for x in scandir(related_items_dir[0].path)]
        else:
            self._related_items = []
        if not pdf_file or not data_file:
            raise ValueError("{} ETD directory is incomplete.".format(an_etd_directory))
        else:
            self._main_file = pdf_file[0].path
            self._data_file = data_file[0].path
        self._metadata = MetadataPackageExtractorBuilder("etd", extraction_config).build().create(self._data_file)

    def check_for_related_items(self):
        if self._related_items:
            return True
        else:
            return False

    def get_main_file(self):
        """a method to return the source path to the main file
        """
        return self._main_file

    def get_relative_path_for_main_file(self):
        return basename(self._main_file)

    def get_metadata(self):
        """a method to return the metadata package for the item
        """
        return self._metadata

    def get_relative_paths_for_related_items(self):
        """a method to return the relative filepaths for related files in an item
        """
        out = []
        for n_item in self._related_items:
            last_directory = basename(dirname(n_item.path))
            file_name = basename(n_item.path)
            out.append(join(last_directory, file_name))
        return out

    def get_related_items(self):
        """a method to return the source filepaths for all related files for the item
        """
        return [x.path for x in self._related_items]

