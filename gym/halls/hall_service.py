from copy import copy

from gym.file_storage import write_json_files
from gym.halls.hall import GymHall


class OperationResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data


class HallManager:
    def __init__(self, repository, class_repository=None, allow_rename=True):
        self.repository = repository
        self.class_repository = class_repository
        self.allow_rename = allow_rename

    def get_hall(self, name):
        hall = self.repository.get_by_name(name)
        if isinstance(hall, GymHall):
            return hall
        return None

    def list_halls(self):
        return self.repository.get_all()

    def create_hall(self, name, capacity, equipment=None, is_active=True):
        try:
            hall = GymHall(name, capacity, equipment, is_active)
        except ValueError as error:
            return OperationResult(False, str(error))
        if self.get_hall(hall.name) is not None:
            return OperationResult(False, f"Hall '{hall.name}' already exists.")
        if not self.repository.add(hall):
            return OperationResult(False, "Hall could not be saved.")
        return OperationResult(True, "Hall created successfully.", hall)

    def update_hall(self, current_name, new_name, capacity, equipment=None):
        hall = self.get_hall(current_name)
        if hall is None:
            return OperationResult(False, f"Hall '{current_name}' was not found.")
        try:
            GymHall.check(new_name, capacity)
        except ValueError as error:
            return OperationResult(False, str(error))
        new_name = new_name.strip()
        if new_name != hall.name and not self.allow_rename:
            return OperationResult(False, "Hall renaming is unavailable until class data can be loaded.")
        if new_name != hall.name and self.get_hall(new_name) is not None:
            return OperationResult(False, f"Hall '{new_name}' already exists.")
        if equipment is None:
            equipment = hall.equipment
        old_name = hall.name
        updated_hall = GymHall(new_name, capacity, equipment, hall.is_active)
        if not self._save_hall(updated_hall, old_name):
            return OperationResult(False, "Hall changes could not be saved.")
        return OperationResult(True, "Hall updated successfully.", updated_hall)

    def deactivate_hall(self, name):
        hall = self.get_hall(name)
        if hall is None:
            return OperationResult(False, f"Hall '{name}' was not found.")
        updated_hall = copy(hall)
        updated_hall.deactivate()
        if not self.repository.update(updated_hall):
            return OperationResult(False, "Hall status could not be saved.")
        return OperationResult(True, "Hall deactivated successfully.", updated_hall)

    def activate_hall(self, name):
        hall = self.get_hall(name)
        if hall is None:
            return OperationResult(False, f"Hall '{name}' was not found.")
        updated_hall = copy(hall)
        updated_hall.activate()
        if not self.repository.update(updated_hall):
            return OperationResult(False, "Hall status could not be saved.")
        return OperationResult(True, "Hall activated successfully.", updated_hall)

    def _save_hall(self, hall, old_name):
        if hall.name == old_name or self.class_repository is None:
            return self.repository.update(hall, old_name)
        halls = self.repository.halls.copy()
        del halls[old_name]
        halls[hall.name] = hall
        classes = self.class_repository.classes.copy()
        for name, gym_class in classes.items():
            if gym_class.hall_name == old_name:
                updated_class = copy(gym_class)
                updated_class.hall_name = hall.name
                classes[name] = updated_class
        try:
            write_json_files([
                (self.repository.data_file, self.repository.to_records(halls.values())),
                (self.class_repository.data_file, self.class_repository.to_records(classes.values())),
            ])
        except (OSError, TypeError, ValueError):
            return False
        self.repository.halls = halls
        self.class_repository.classes = classes
        return True
