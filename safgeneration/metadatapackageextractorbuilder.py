
from .metadataextractor import MetadataExtractor

class MetadataPackageExtractorBuilder(object):
    def __init__(self, choice, config):
        self.choice = choice
        self.config = config

    def build(self):
        if self.choice == 'etd':
            return MetadataExtractor(self.config)
        else:
            raise ValueError("{} is not a valid metadata package builder choice".format(self.choice))

