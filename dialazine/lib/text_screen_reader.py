import os

class TextScreenReader:
    def __init__(self, root_directory):
        self.root_directory = root_directory
    def read_file_name(self, path):
        full_path = "%s/%s" % (self.root_directory, path)
        with open(full_path, 'r') as f:
            full_file = f.readlines()
            f.close()
        return full_file
    def does_file_exist(self, file_path):
        return os.path.exists("%s/%s" % (self.root_directory, file_path))
