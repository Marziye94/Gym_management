import json
import os
from gym.models.gym_class import GymClass


DEFAULT_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classes.json")


class ClassRepository:
    def __init__(self, data_file=DEFAULT_DATA_FILE):
        self.data_file = data_file
        self.classes = {}
        self.load()

    def load(self):
        self.classes = {}
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                is_active = True
                if item.get("status") == "Inactive":
                    is_active = False

                gym_class = GymClass(
                    name=item["title"],
                    exercise=item["sport_type"],
                    coach_name=item["coach"],
                    hall_name=item["hall"],
                    day=item["day"],
                    time=item["time"],
                    capacity=item["total_capacity"],
                    remaining_capacity=item["remaining_capacity"],
                    is_active=is_active
                )
                self.classes[gym_class.name] = gym_class
        except Exception:
            print("Error: Could not read stored class data.")

    def save(self):
        try:
            folder = os.path.dirname(self.data_file)
            if folder != "":
                os.makedirs(folder, exist_ok=True)

            data_list = []
            for gym_class in self.classes.values():
                status = "Active"
                if not gym_class.is_active:
                    status = "Inactive"

                item = {
                    "title": gym_class.name,
                    "sport_type": gym_class.exercise,
                    "coach": gym_class.coach_name,
                    "hall": gym_class.hall_name,
                    "day": gym_class.day,
                    "time": gym_class.time,
                    "total_capacity": gym_class.capacity,
                    "remaining_capacity": gym_class.remaining_capacity,
                    "status": status
                }
                data_list.append(item)

            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(data_list, file, indent=4)
            return True
        except Exception:
            print("Error: Could not save class data.")
            return False

    def add(self, gym_class):
        if gym_class.name in self.classes:
            return False
        self.classes[gym_class.name] = gym_class
        if not self.save():
            del self.classes[gym_class.name]
            return False
        return True

    def get_class(self, class_name):
        if not class_name or not isinstance(class_name, str):
            return None
        return self.classes.get(class_name.strip(), None)

    def get_all(self):
        return list(self.classes.values())

    def update(self, gym_class, old_name=None):
        target_name = old_name.strip() if old_name else gym_class.name
        if target_name not in self.classes:
            return False
        previous_classes = self.classes.copy()
        if target_name != gym_class.name:
            if gym_class.name in self.classes:
                return False
            del self.classes[target_name]
        self.classes[gym_class.name] = gym_class
        if not self.save():
            self.classes = previous_classes
            return False
        return True