from gym.models.gym_hall import GymHall


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

    def create_hall(self, name, capacity, equipment=None):
        try:
            hall = GymHall(name, capacity, equipment)
        except ValueError as error:
            return OperationResult(False, str(error))
        if self.get_hall(hall.name) is not None:
            return OperationResult(False, f"Hall '{hall.name}' already exists.")
        self.repository.add(hall)
        return OperationResult(True, "Hall created.", hall)

    def update_hall(self, name, capacity, equipment=None):
        hall = self.get_hall(name)
        if hall is None:
            return OperationResult(False, f"Hall '{name}' was not found.")
        try:
            hall.update_details(name, capacity, equipment)
        except ValueError as error:
            return OperationResult(False, str(error))
        self.repository.update(hall)
        return OperationResult(True, "Hall updated.", hall)

    def deactivate_hall(self, name):
        hall = self.get_hall(name)
        if hall is None:
            return OperationResult(False, f"Hall '{name}' was not found.")
        hall.deactivate()
        return OperationResult(True, "Hall deactivated.", hall)

    def activate_hall(self, name):
        hall = self.get_hall(name)
        if hall is None:
            return OperationResult(False, f"Hall '{name}' was not found.")
        hall.activate()
        return OperationResult(True, "Hall activated.", hall)
