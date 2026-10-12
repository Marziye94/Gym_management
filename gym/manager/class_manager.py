from gym.models.gym_class import GymClass


class OperationResult:

    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data


class ClassManager:
    def __init__(self, repository, check_coach_active_fn, check_hall_active_fn):
        self.repository = repository
        self.check_coach = check_coach_active_fn
        self.check_hall = check_hall_active_fn

    def create_class(self, name, exercise, coach_name, hall_name, schedule, capacity):
        try:
            if self.repository.get_class(name):
                return OperationResult(False, f"A class named {name} already exists.")

            if not self.check_coach(coach_name):
                return OperationResult(False, f"Coach {coach_name} does not exist or is inactive.")

            if not self.check_hall(hall_name):
                return OperationResult(False, f"Hall {hall_name} does not exist or is inactive.")

            new_class = GymClass(name, exercise, coach_name,
                                 hall_name, schedule, capacity)
            self.repository.add(new_class)

            return OperationResult(True, "Class created successfully.", new_class)

        except ValueError as e:
            return OperationResult(False, str(e))
        except Exception as e:
            return OperationResult(False, f"An unknown error occurred: {str(e)}")

    def get_class(self, name):
        gym_class = self.repository.get_class(name)
        if gym_class:
            return OperationResult(True, "Class found.", gym_class)
        return OperationResult(False, "Class not found.")

    def list_classes(self):
        classes = self.repository.get_all()
        return OperationResult(True, f"{len(classes)} classes found.", classes)

    def update_class(self, original_name, new_name, exercise, schedule, capacity):
        try:
            gym_class = self.repository.get_class(original_name)
            if not gym_class:
                return OperationResult(False, "Class not found for editing.")

            if original_name != new_name and self.repository.get_class(new_name):
                return OperationResult(False, f"A class with the new name '{new_name}' already exists.")

            gym_class.update_details(new_name, exercise, schedule, capacity)

            if original_name != new_name:
                self.repository.classes.pop(original_name)
                self.repository.add(gym_class)
            else:
                self.repository.update(gym_class)

            return OperationResult(True, "Class details updated successfully.", gym_class)
        except ValueError as e:
            return OperationResult(False, str(e))

    def assign_coach(self, class_name, coach_name):
        try:
            gym_class = self.repository.get_class(class_name)
            if not gym_class:
                return OperationResult(False, "Class not found.")

            if not self.check_coach(coach_name):
                return OperationResult(False, f"Coach {coach_name} does not exist or is inactive.")

            gym_class.assign_coach(coach_name)
            self.repository.update(gym_class)
            return OperationResult(True, f"Coach '{coach_name}' was successfully assigned to the class.", gym_class)
        except ValueError as e:
            return OperationResult(False, str(e))

    def assign_hall(self, class_name, hall_name):
        try:
            gym_class = self.repository.get_class(class_name)
            if not gym_class:
                return OperationResult(False, "Class not found.")

            if not self.check_hall(hall_name):
                return OperationResult(False, f"Hall {hall_name} does not exist or is inactive.")

            gym_class.assign_hall(hall_name)
            self.repository.update(gym_class)
            return OperationResult(True, f"Hall '{hall_name}' was successfully assigned to the class.", gym_class)
        except ValueError as e:
            return OperationResult(False, str(e))

    def deactivate_class(self, class_name):
        gym_class = self.repository.get_class(class_name)
        if not gym_class:
            return OperationResult(False, "Class not found.")

        gym_class.deactivate()
        self.repository.update(gym_class)
        return OperationResult(True, "Class deactivated successfully.", gym_class)

    def activate_class(self, class_name):
        gym_class = self.repository.get_class(class_name)
        if not gym_class:
            return OperationResult(False, "Class not found.")

        gym_class.activate()
        self.repository.update(gym_class)
        return OperationResult(True, "Class activated successfully.", gym_class)
