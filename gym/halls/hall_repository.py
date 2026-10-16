import json
import os

from gym.file_storage import write_json_files

from gym.halls.hall import GymHall

DEFAULT_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "halls.json"))


class HallRepository:
    def __init__(self, data_file=DEFAULT_DATA_FILE):
        self.data_file = data_file
        self.halls = {}
        self.load()

    def load(self):
        self.load_failed = False
        self.halls = {}
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                records = json.load(file)
        except (OSError, ValueError):
            self.load_failed = True
            print("Stored hall data could not be read. Starting with an empty hall list.")
            return
        if type(records) is not list:
            self.load_failed = True
            print("Stored hall data is invalid. Starting with an empty hall list.")
            return
        for record in records:
            try:
                hall = GymHall(record["name"], record["capacity"],
                               record["equipment"], record["is_active"])
            except (KeyError, TypeError, ValueError):
                self.load_failed = True
                print("An invalid hall record was skipped.")
                continue
            self.halls[hall.name] = hall

    def to_records(self, halls=None):
        if halls is None:
            halls = self.halls.values()
        records = []
        for hall in halls:
            records.append({
                "name": hall.name,
                "capacity": hall.capacity,
                "equipment": hall.equipment,
                "is_active": hall.is_active,
            })
        return records

    def save(self):
        try:
            write_json_files([(self.data_file, self.to_records())])
            return True
        except (OSError, TypeError, ValueError):
            return False

    def add(self, hall):
        if hall.name in self.halls:
            return False
        self.halls[hall.name] = hall
        if not self.save():
            del self.halls[hall.name]
            return False
        return True

    def get_by_name(self, hall_name):
        if hall_name in self.halls:
            return self.halls[hall_name]
        return f"Hall '{hall_name}' was not found."

    def get_all(self):
        return list(self.halls.values())

    def update(self, hall, old_name=None):
        if old_name is None:
            old_name = hall.name
        if old_name not in self.halls:
            return False
        if old_name != hall.name and hall.name in self.halls:
            return False
        previous_halls = self.halls.copy()
        del self.halls[old_name]
        self.halls[hall.name] = hall
        if not self.save():
            self.halls = previous_halls
            return False
        return True
