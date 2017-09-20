from os import scandir
from os import listdir
from os.path import basename, dirname, exists, join

class SimpleArchiveFormatValidator(object):
    def __init__(self, saf_root, total_expected):
        if exists(saf_root):
            self.saf_directory = saf_root
        else:
            raise ValueError("{} does not exist. Can only validate a SimpleArchiveFormat directory that exists.")
        self._validation = True
        self._total_expected = total_expected
        self._errors = []

    def _validate_related_items(self, item_path):
        translate_table = str.maketrans("\\", "/")
        contents_file = join(item_path, 'contents')
        contents_file_lines = []
        out = True
        with open(contents_file, 'r', encoding="utf-8") as read_file:
            contents_file_lines = [x.strip() for x in read_file.readlines()]
        relevant_lines = [x for x in contents_file_lines if not x.endswith('pdf')]
        if relevant_lines:
            related_dir = dirname(join(item_path, relevant_lines[0]))
            related_dir_name = basename(related_dir)
            related_dir_contents = [join(related_dir_name, x).translate(translate_table) for x in listdir(related_dir)]
            if set(relevant_lines) - set(related_dir_contents):
                out = False
        return out

    def _validate_saf_item(self, item_path):
        item_id = basename(item_path)
        contents = [x.path for x in scandir(item_path)]
        out = True
        if not [x for x in contents if x.endswith("contents")]:
            self._errors.append("{} is missing contents file.".format(item_id))
            out = False
        elif not [x for x in contents if x.endswith(".pdf")]:
            self._errors.append("{} is missing the main file.".format(item_id))
            out = False
        elif not self._validate_related_items(item_path):
            self._errors.append("{} has a discrepancy between source related files and dest related files.".format(item_id))
            out = False
        self._validation &= out

    def validate(self):
        count = 0
        for n_thing in scandir(self.saf_directory):
            if n_thing.is_dir():
                self._validate_saf_item(n_thing.path)
            count += 1
        if count != self._total_expected:
            self._errors.append("{} items were expected but {} were found.".\
            format(str(self._total_expected), count))

    def get_errors(self):
        """ a method to get a generator from the errors that result from publishing
        """
        for error in self._errors:
            yield error

    def get_validation(self):
        return self._validation