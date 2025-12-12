import json
import os

class Database_Management:
    def __init__(self, filename="database.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)

    def load_data(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)