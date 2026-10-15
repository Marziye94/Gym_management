from copy import copy

from gym.file_storage import write_json_files
from gym.classes.gym_class import GymClass


class OperationResult:
    def __init__(self, success: bool, message: str, data=None):
        self.success = success
        self.message = message
        self.data = data


class ClassManager:
    def __init__(self, repository, check_coach_active_fn, check_hall_active_fn,
                 enrollment_repository=None, workout_repository=None, allow_rename=True):
        self.repository = repository
        self.check_coach = check_coach_active_fn
        self.check_hall = check_hall_active_fn
        self.enrollment_repository = enrollment_repository
        self.workout_repository = workout_repository
        self.allow_rename = allow_rename

    def create_class(self, name, exercise, coach_name, hall_name, day, time, capacity):
        try:
            clean_name = str(name).strip() if name else ""
            clean_coach = str(coach_name).strip() if coach_name else ""
            clean_hall = str(hall_name).strip() if hall_name else ""

            new_class = GymClass(name, exercise, coach_name,
                                 hall_name, day, time, capacity)

            if self.repository.get_class(clean_name):
                return OperationResult(False, f"Class '{clean_name}' already exists.")

            if not self.check_coach(clean_coach):
                return OperationResult(False, f"Coach '{clean_coach}' does not exist or is inactive.")

            if not self.check_hall(clean_hall):
                return OperationResult(False, f"Hall '{clean_hall}' does not exist or is inactive.")

            if not self.repository.add(new_class):
                return OperationResult(False, "Could not save the class.")

            return OperationResult(True, "Class created successfully.", new_class)

        except ValueError as error:
            return OperationResult(False, str(error))
        except Exception as error:
            return OperationResult(False, f"Unexpected error: {str(error)}")

    def get_class(self, name):
        gym_class = self.repository.get_class(name)
        if gym_class:
            gym_class.remaining_capacity = max(0, gym_class.capacity - self._registered_count(gym_class))
            return OperationResult(True, "Class found.", gym_class)
        return OperationResult(False, f"Class '{name}' was not found.")

    def list_classes(self):
        classes = self.repository.get_all()
        for gym_class in classes:
            gym_class.remaining_capacity = max(0, gym_class.capacity - self._registered_count(gym_class))
        return OperationResult(True, f"{len(classes)} classes found.", classes)

    def update_class(
        self,
        current_name,
        new_name,
        new_exercise,
        new_coach_name,
        new_hall_name,
        new_day,
        new_time,
        new_capacity,
    ):
        try:
            gym_class = self.repository.get_class(current_name)
            if not gym_class:
                return OperationResult(False, f"Class '{current_name}' was not found.")

            clean_current = gym_class.name
            clean_new_name = str(new_name).strip() if new_name else ""
            if clean_new_name != clean_current and not self.allow_rename:
                return OperationResult(False, "Class renaming is unavailable until enrollment and workout data can be loaded.")
            clean_coach = str(new_coach_name).strip() if new_coach_name else ""
            clean_hall = str(new_hall_name).strip() if new_hall_name else ""

            GymClass(
                new_name,
                new_exercise,
                new_coach_name,
                new_hall_name,
                new_day,
                new_time,
                new_capacity,
            )

            if clean_current != clean_new_name and self.repository.get_class(clean_new_name):
                return OperationResult(False, f"Class '{clean_new_name}' already exists.")

            if not self.check_coach(clean_coach):
                return OperationResult(False, f"Coach '{clean_coach}' does not exist or is inactive.")

            if not self.check_hall(clean_hall):
                return OperationResult(False, f"Hall '{clean_hall}' does not exist or is inactive.")

            registered_count = self._registered_count(gym_class)
            if new_capacity < registered_count:
                return OperationResult(False, "Capacity cannot be less than the number of registered members.")

            updated_class = GymClass(
                gym_class.name,
                gym_class.exercise,
                gym_class.coach_name,
                gym_class.hall_name,
                gym_class.day,
                gym_class.time,
                gym_class.capacity,
                max(0, gym_class.capacity - registered_count),
                gym_class.is_active,
            )
            updated_class.update_details(
                new_name,
                new_exercise,
                new_coach_name,
                new_hall_name,
                new_day,
                new_time,
                new_capacity,
            )
            if not self._save_class(updated_class, clean_current):
                return OperationResult(False, "Could not update the class.")

            return OperationResult(True, "Class updated successfully.", updated_class)

        except ValueError as error:
            return OperationResult(False, str(error))
        except Exception as error:
            return OperationResult(False, f"Unexpected error: {str(error)}")

    def assign_coach(self, class_name, coach_name):
        try:
            gym_class = self.repository.get_class(class_name)
            if not gym_class:
                return OperationResult(False, f"Class '{class_name}' was not found.")

            clean_coach = str(coach_name).strip() if coach_name else ""
            if not self.check_coach(clean_coach):
                return OperationResult(False, f"Coach '{clean_coach}' does not exist or is inactive.")

            previous_coach = gym_class.coach_name
            gym_class.assign_coach(clean_coach)
            if not self.repository.update(gym_class):
                gym_class.coach_name = previous_coach
                return OperationResult(False, "Could not save the coach assignment.")
            return OperationResult(True, "Coach assigned successfully.", gym_class)
        except ValueError as error:
            return OperationResult(False, str(error))

    def assign_hall(self, class_name, hall_name):
        try:
            gym_class = self.repository.get_class(class_name)
            if not gym_class:
                return OperationResult(False, f"Class '{class_name}' was not found.")

            clean_hall = str(hall_name).strip() if hall_name else ""
            if not self.check_hall(clean_hall):
                return OperationResult(False, f"Hall '{clean_hall}' does not exist or is inactive.")

            previous_hall = gym_class.hall_name
            gym_class.assign_hall(clean_hall)
            if not self.repository.update(gym_class):
                gym_class.hall_name = previous_hall
                return OperationResult(False, "Could not save the hall assignment.")
            return OperationResult(True, "Hall assigned successfully.", gym_class)
        except ValueError as error:
            return OperationResult(False, str(error))

    def deactivate_class(self, class_name):
        gym_class = self.repository.get_class(class_name)
        if not gym_class:
            return OperationResult(False, f"Class '{class_name}' was not found.")

        previous_status = gym_class.is_active
        gym_class.deactivate()
        if not self.repository.update(gym_class):
            gym_class.is_active = previous_status
            return OperationResult(False, "Could not save the class status.")
        return OperationResult(True, "Class deactivated successfully.", gym_class)

    def activate_class(self, class_name):
        gym_class = self.repository.get_class(class_name)
        if not gym_class:
            return OperationResult(False, f"Class '{class_name}' was not found.")

        previous_status = gym_class.is_active
        gym_class.activate()
        if not self.repository.update(gym_class):
            gym_class.is_active = previous_status
            return OperationResult(False, "Could not save the class status.")
        return OperationResult(True, "Class activated successfully.", gym_class)

    def _registered_count(self, gym_class):
        if self.enrollment_repository is None:
            return gym_class.capacity - gym_class.remaining_capacity
        count = 0
        for enrollment in self.enrollment_repository.get_all():
            if enrollment.class_name == gym_class.name and enrollment.is_active:
                count += 1
        return count

    def _save_class(self, gym_class, old_name):
        if gym_class.name == old_name:
            return self.repository.update(gym_class, old_name)
        classes = self.repository.classes.copy()
        del classes[old_name]
        classes[gym_class.name] = gym_class
        files = [(self.repository.data_file, self.repository.to_records(classes.values()))]
        enrollments = {}
        plans = {}
        if self.enrollment_repository is not None:
            enrollments = self.enrollment_repository.enrollments.copy()
            for enrollment_id, enrollment in enrollments.items():
                if enrollment.class_name == old_name:
                    updated_enrollment = copy(enrollment)
                    updated_enrollment.class_name = gym_class.name
                    enrollments[enrollment_id] = updated_enrollment
            files.append((self.enrollment_repository.file_path,
                          self.enrollment_repository.to_records(enrollments.values())))
        if self.workout_repository is not None:
            plans = self.workout_repository.plans.copy()
            for plan_id, plan in plans.items():
                if plan.class_id == old_name:
                    updated_plan = copy(plan)
                    updated_plan.class_id = gym_class.name
                    plans[plan_id] = updated_plan
            files.append((self.workout_repository.data_file,
                          self.workout_repository.to_records(plans.values())))
        try:
            write_json_files(files)
        except (OSError, TypeError, ValueError):
            return False
        self.repository.classes = classes
        if self.enrollment_repository is not None:
            self.enrollment_repository.enrollments = enrollments
        if self.workout_repository is not None:
            self.workout_repository.plans = plans
        return True
