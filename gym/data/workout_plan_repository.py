import json
import os

from gym.models.workout_plan import Exercise, WorkoutPlan

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workout_plans.json")


class WorkoutPlanRepository:
    def __init__(self, data_file=DEFAULT_DATA_FILE):
        self.data_file = data_file
        self.plans = {}
        self.next_id = 1
        self.load()

    def load(self):
        self.plans = {}
        self.next_id = 1
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, ValueError):
            print("Stored workout plan data could not be read. Starting with no plans.")
            return
        if type(data) is not dict or type(data.get("plans")) is not list:
            print("Stored workout plan data is invalid. Starting with no plans.")
            return

        stored_next_id = data.get("next_id")
        if type(stored_next_id) is int and stored_next_id > 0:
            self.next_id = stored_next_id

        for record in data["plans"]:
            if type(record) is dict and type(record.get("plan_id")) is int:
                self.next_id = max(self.next_id, record["plan_id"] + 1)
            plan = self.plan_from_dict(record)
            if plan is None:
                print("An invalid workout plan record was skipped.")
                continue
            self.plans[plan.plan_id] = plan

    def plan_from_dict(self, record):
        try:
            exercises = []
            for item in record["exercises"]:
                exercises.append(Exercise(item["name"], item["sets"], item["repetitions"],
                                          item["rest_time"], item["description"]))
            return WorkoutPlan(record["plan_id"], record["coach_username"], record["class_id"],
                               record["member_username"], exercises)
        except (KeyError, TypeError, ValueError):
            return None

    def plan_to_dict(self, plan):
        exercises = []
        for exercise in plan.exercises:
            exercises.append({
                "name": exercise.name,
                "sets": exercise.sets,
                "repetitions": exercise.repetitions,
                "rest_time": exercise.rest_time,
                "description": exercise.description,
            })
        return {
            "plan_id": plan.plan_id,
            "coach_username": plan.coach_username,
            "class_id": plan.class_id,
            "member_username": plan.member_username,
            "exercises": exercises,
        }

    def save(self):
        data = {
            "next_id": self.next_id,
            "plans": [self.plan_to_dict(plan) for plan in self.plans.values()],
        }
        try:
            folder = os.path.dirname(self.data_file)
            if folder:
                os.makedirs(folder, exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except OSError:
            print("Workout plan data could not be saved.")
            return False

    def generate_id(self):
        plan_id = self.next_id
        self.next_id += 1
        return plan_id

    def add(self, plan):
        if plan.plan_id in self.plans:
            return f"Workout plan {plan.plan_id} already exists."
        self.plans[plan.plan_id] = plan
        self.save()
        return f"Workout plan {plan.plan_id} was added."

    def update(self, plan):
        if plan.plan_id not in self.plans:
            return f"Workout plan {plan.plan_id} was not found."
        self.plans[plan.plan_id] = plan
        self.save()
        return f"Workout plan {plan.plan_id} was updated."

    def get_by_id(self, plan_id):
        return self.plans.get(plan_id)

    def get_all(self):
        return list(self.plans.values())

    def find(self, coach_username, class_id, member_username):
        for plan in self.plans.values():
            if (plan.coach_username == coach_username and plan.class_id == class_id
                    and plan.member_username == member_username):
                return plan
        return None