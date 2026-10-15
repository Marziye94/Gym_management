from gym.halls.hall import GymHall


class OperationResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data


class HallManager:
    def __init__(self, repository):
        self.repository = repository

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
            return OperationResult(False, "Hall could not be saved. Please try again.")
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
        if new_name != hall.name and self.get_hall(new_name) is not None:
            return OperationResult(False, f"Hall '{new_name}' already exists.")
        if equipment is None:
            equipment = hall.equipment
        old_name = hall.name
        old_capacity = hall.capacity
        old_equipment = list(hall.equipment)
        hall.update_details(new_name, capacity, equipment)
        if not self.repository.update(hall, old_name):
            hall.update_details(old_name, old_capacity, old_equipment)
            return OperationResult(False, "Hall changes could not be saved. Please try again.")
        return OperationResult(True, "Hall updated successfully.", hall)

    def deactivate_hall(self, name):
        hall = self.get_hall(name)
        if hall is None:
            return OperationResult(False, f"Hall '{name}' was not found.")
        was_active = hall.is_active
        hall.deactivate()
        if not self.repository.update(hall):
            hall.is_active = was_active
            return OperationResult(False, "Hall status could not be saved. Please try again.")
        return OperationResult(True, "Hall deactivated successfully.", hall)

    def activate_hall(self, name):
        hall = self.get_hall(name)
        if hall is None:
            return OperationResult(False, f"Hall '{name}' was not found.")
        was_active = hall.is_active
        hall.activate()
        if not self.repository.update(hall):
            hall.is_active = was_active
            return OperationResult(False, "Hall status could not be saved. Please try again.")
        return OperationResult(True, "Hall activated successfully.", hall)