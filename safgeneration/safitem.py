
from os.path import basename, dirname, exists, join
from shutil import copyfile

from .utilities import make_a_directory

class SAFItem(object):
    def __init__(self, item_object, metadata_object):
        self.item = item_object
        self.metadata = metadata_object
        self._errors = []

    def _copy_source_to_saf(self, src, dest):
         if not exists(dest) and exists(src):
                try:
                    copyfile(src, dest)
                except OSError:
                    self._errors.append("{} could not be copied to {}".format(src, dest))
         else:
             pass

    def _write_a_contents_file(self, an_item, write_file_path):
        rel_items = an_item.get_relative_paths_for_related_items()
        translate_table = str.maketrans("\\", "/")
        pdf = an_item.get_relative_path_for_main_file()
        pdf = pdf.translate(translate_table)
        with open(write_file_path, 'w+', encoding="utf-8") as write_file:
            write_file.write("{}\n".format(pdf))
            for n_item in rel_items:
                n_item = n_item.translate(translate_table)
                write_file.write("{}\n".format(n_item))


    def publish(self, item_root):
        make_a_directory(item_root)
        dc_file_path = join(item_root, "dublin_core.xml")
        contents_file_path = join(item_root, "contents")
        self.metadata.write_out_to_a_file(dc_file_path)
        self._write_a_contents_file(self.item, contents_file_path)
        main_file_src = self.item.get_main_file()
        main_file_dest = join(item_root, basename(main_file_src))
        self._copy_source_to_saf(main_file_src, main_file_dest)
        if self.item.check_for_related_items():
            rel_items = self.item.get_related_items()
            subdir = join(item_root, basename(dirname(rel_items[0])))
            make_a_directory(subdir)
            for rel_item in rel_items:
                dest = join(item_root, subdir, basename(rel_item))
                src = rel_item
                self._copy_source_to_saf(src, dest)
