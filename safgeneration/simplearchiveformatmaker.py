"""
"""
from collections import deque
from os import mkdir, scandir
from os import getcwd
from os.path import basename, dirname, exists, join
from shutil import copyfile

from .safitem import SAFItem
from .utilities import make_a_directory

class SimpleArchiveFormatMaker(object):
    def __init__(self, output_root=getcwd()):
        self._items = deque()
        self._total_items = 0
        self.root = output_root
        self._errors = []

    def publish(self):
        """a method to create a SAF directory in your chosen output directory
        """
        make_a_directory(join(self.root, 'SimpleArchiveFormat'))
        item_count = 1
        while item_count <= self._total_items:
            item = self._items.pop()
            item_root = join(self.root, 'SimpleArchiveFormat', 'item_' + str(item_count).zfill(3))
            make_a_directory(item_root)
            item.publish(item_root)
            if item.item.check_for_related_items():
                rel_items = item.item.get_related_items()
                subdir = join(item_root, basename(dirname(rel_items[0])))
                make_a_directory(subdir)
            item_count += 1

    def get_errors(self):
        """ a method to get a generator from the errors that result from publishing
        """
        for error in self._errors:
            yield error

    def get_saf_root(self):
        return join(self.root, "SimpleArchiveFormat")

    def get_total_items(self):
        return self._total_items

    def add_item(self, item, metadata):
        """a method to add an item to the safmaker
        """
        self._items.appendleft(SAFItem(item, metadata))
        self._total_items += 1