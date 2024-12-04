import os


class FileHandler:
    @staticmethod
    def save_file(content, path):
        with open(path, 'w') as file:
            file.write(content)

    @staticmethod
    def read_file(path):
        if not os.path.exists(path):
            return None
        with open(path, 'r') as file:
            return file.read()
