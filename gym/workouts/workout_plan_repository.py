import json
import os
import copy
from gym.workouts.workout_plan import Exercise, WorkoutPlan

DEFAULT_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "workout_plans.json"))

class WorkoutPlanRepository:
    def __init__(self, data_file=DEFAULT_DATA_FILE):
        self.data_file = data_file
        self.plans = {}
        self.next_id = 1
        self.load()

    def load(self):
        self.load_failed = False
        self.plans = {}
        self.next_id = 1
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, ValueError):
            self.load_failed = True
            return

        try:
            plans_dict = {}
            max_id = 0
            for record in data.get("plans", []):
                exercises = [
                    Exercise(
                        name=ex.get("name"),
                        sets=ex.get("sets"),
                        reps=ex.get("reps"),
                        rest_time=ex.get("rest_time"),
                        description=ex.get("description")
                    )
                    for ex in record.get("exercises", [])
                ]
                plan = WorkoutPlan(
                    member_username=record.get("member_username"),
                    exercises=exercises,
                    plan_id=record.get("id")
                )
                if plan.plan_id:
                    if plan.plan_id > max_id:
                        max_id = plan.plan_id
                plans_dict[plan.member_username] = plan
            self.plans = plans_dict
            self.next_id = max_id + 1
        except (TypeError, ValueError, KeyError):
            self.load_failed = True

    def save(self):
        try:
            folder = os.path.dirname(self.data_file)
            if folder and not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
            
            plans_list = []
            for plan in self.plans.values():
                exercises_list = [
                    {
                        "name": ex.name,
                        "sets": ex.sets,
                        "reps": ex.reps,
                        "rest_time": ex.rest_time,
                        "description": ex.description
                    }
                    for ex in plan.exercises
                ]
                plans_list.append({
                    "id": plan.plan_id,
                    "member_username": plan.member_username,
                    "exercises": exercises_list
                })
            
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump({"plans": plans_list}, file, indent=4)
            return True
        except (OSError, TypeError):
            return False

    def add(self, plan):
        previous_plans = copy.deepcopy(self.plans)
        previous_next_id = self.next_id

        if plan.plan_id is None:
            plan.plan_id = self.next_id
            self.next_id += 1

        self.plans[plan.member_username] = plan

        if not self.save():
            self.plans = previous_plans
            self.next_id = previous_next_id
            return False, "Error: Could not save workout plan to storage."
        
        return True, "Workout plan added successfully."

    def update(self, plan):
        previous_plans = copy.deepcopy(self.plans)

        self.plans[plan.member_username] = plan

        if not self.save():
            self.plans = previous_plans
            return False, "Error: Could not update workout plan in storage."
        
        return True, "Workout plan updated successfully."

    def get_plan_by_username(self, username):
        return self.plans.get(username)
