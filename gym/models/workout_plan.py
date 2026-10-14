class Exercise:
    def __init__(self, name, sets, repetitions, rest_time, description=""):
        self.check(name, sets, repetitions, rest_time, description)
        self.name = name.strip()
        self.sets = sets
        self.repetitions = repetitions
        self.rest_time = rest_time
        self.description = description.strip()

    @staticmethod
    def check(name, sets, repetitions, rest_time, description):
        if type(name) is not str or name.strip() == "":
            raise ValueError("Exercise name must not be empty.")
        if type(sets) is not int or sets <= 0:
            raise ValueError("Sets must be a positive integer.")
        if type(repetitions) is not int or repetitions <= 0:
            raise ValueError("Repetitions must be a positive integer.")
        if type(rest_time) not in (int, float) or rest_time < 0:
            raise ValueError("Rest time must be a non-negative number.")
        if type(description) is not str:
            raise ValueError("Description must be text.")

    def update(self, name, sets, repetitions, rest_time, description):
        self.check(name, sets, repetitions, rest_time, description)
        self.name = name.strip()
        self.sets = sets
        self.repetitions = repetitions
        self.rest_time = rest_time
        self.description = description.strip()


class WorkoutPlan:
    def __init__(self, plan_id, coach_username, class_id, member_username, exercises=None):
        if type(plan_id) is not int or plan_id <= 0:
            raise ValueError("Plan ID must be a positive integer.")
        if type(coach_username) is not str or coach_username.strip() == "":
            raise ValueError("Coach username must not be empty.")
        if type(member_username) is not str or member_username.strip() == "":
            raise ValueError("Member username must not be empty.")
        if class_id is None or class_id == "":
            raise ValueError("Class ID must not be empty.")
        self.plan_id = plan_id
        self.coach_username = coach_username
        self.class_id = class_id
        self.member_username = member_username
        self.exercises = exercises or []

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def get_exercise(self, number):
        if type(number) is not int or number < 1 or number > len(self.exercises):
            return None
        return self.exercises[number - 1]