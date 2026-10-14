from gym.models.workout_plan import Exercise, WorkoutPlan


class OperationResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data


class WorkoutPlanManager:
    def __init__(self, plan_repository, class_repository, enrollment_lookup):
        self.plan_repository = plan_repository
        self.class_repository = class_repository
        self.enrollment_lookup = enrollment_lookup

    def get_coach_username(self, coach):
        if hasattr(coach, "username"):
            if getattr(coach, "role", "Coach") != "Coach":
                return None
            return coach.username
        if type(coach) is str and coach.strip() != "":
            return coach.strip()
        return None

    def get_active_members(self, class_name):
        try:
            members = self.enrollment_lookup.get_active_member_usernames(class_name)
        except Exception:
            print("Enrollment data could not be read.")
            return []
        return list(members or [])

    def get_coach_classes(self, coach):
        username = self.get_coach_username(coach)
        if username is None:
            return []
        classes = []
        for gym_class in self.class_repository.get_all():
            if gym_class.coach_name.lower() == username.lower():
                classes.append(gym_class)
        return classes

    def get_coach_class(self, coach, class_name):
        username = self.get_coach_username(coach)
        if username is None:
            return OperationResult(False, "Only an authenticated coach can do this.")
        gym_class = self.class_repository.get_class(class_name)
        if gym_class is None:
            return OperationResult(False, f"Class '{class_name}' was not found.")
        if gym_class.coach_name.lower() != username.lower():
            return OperationResult(False, f"Class '{class_name}' is not one of your classes.")
        return OperationResult(True, "Class found.", gym_class)

    def check_member(self, coach, class_name, member_username):
        result = self.get_coach_class(coach, class_name)
        if not result.success:
            return result
        gym_class = result.data
        if member_username not in self.get_active_members(gym_class.name):
            return OperationResult(
                False, f"Member '{member_username}' has no active enrollment in '{gym_class.name}'.")
        return OperationResult(True, "Member found.", gym_class)

    def get_plan(self, coach, class_name, member_username):
        result = self.check_member(coach, class_name, member_username)
        if not result.success:
            return result
        username = self.get_coach_username(coach)
        plan = self.plan_repository.find(username, result.data.name, member_username)
        if plan is None:
            return OperationResult(False, f"No workout plan exists for '{member_username}' in this class.")
        return OperationResult(True, "Workout plan found.", plan)

    def create_plan(self, coach, class_name, member_username):
        result = self.check_member(coach, class_name, member_username)
        if not result.success:
            return result
        username = self.get_coach_username(coach)
        class_id = result.data.name
        if self.plan_repository.find(username, class_id, member_username) is not None:
            return OperationResult(False, f"A workout plan for '{member_username}' already exists.")
        plan = WorkoutPlan(self.plan_repository.generate_id(), username, class_id, member_username)
        self.plan_repository.add(plan)
        return OperationResult(True, "Workout plan created successfully.", plan)

    def add_exercise(self, coach, class_name, member_username, name, sets, repetitions, rest_time, description):
        result = self.get_plan(coach, class_name, member_username)
        if not result.success:
            return result
        plan = result.data
        try:
            exercise = Exercise(name, sets, repetitions, rest_time, description)
        except ValueError as error:
            return OperationResult(False, str(error))
        plan.add_exercise(exercise)
        self.plan_repository.update(plan)
        return OperationResult(True, "Exercise added successfully.", plan)

    def update_exercise(self, coach, class_name, member_username, number,
                        name, sets, repetitions, rest_time, description):
        result = self.get_plan(coach, class_name, member_username)
        if not result.success:
            return result
        plan = result.data
        exercise = plan.get_exercise(number)
        if exercise is None:
            return OperationResult(False, f"Exercise number {number} was not found.")
        try:
            exercise.update(name, sets, repetitions, rest_time, description)
        except ValueError as error:
            return OperationResult(False, str(error))
        self.plan_repository.update(plan)
        return OperationResult(True, "Exercise updated successfully.", plan)