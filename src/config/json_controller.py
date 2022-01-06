import json


class FileJSON:
    def __init__(self, path):
        self.path = path

    def get_json(self):
        with open(self.path) as file:
            return json.load(file)

    def set_json(self, data):
        with open(self.path, "w+") as file:
            json.dump(data, file)
