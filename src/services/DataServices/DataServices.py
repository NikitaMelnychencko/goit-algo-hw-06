import json
from pathlib import Path

class DataServices:
    def __init__(self):
        self.name = "contacts.json"
        self.path = Path("./data/" + self.name)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def get_init_data(self):
        if not self.path.exists():
            return {}
        try:
            with open(self.path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def save_data(self, data):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
