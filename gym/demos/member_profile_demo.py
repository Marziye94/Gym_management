import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from menus.member_menus.profile import display_member_profile
from menus.member_menus.view_workout_plan import display_workout_plan

class MockUser:
    def __init__(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email
        self.is_active = True

class MockUserManager:
    def __init__(self):
        self.users = {
            "reza123": MockUser("Reza Ahmadi", "reza123", "reza@test.com"),
            "sara123": MockUser("Sara Kamali", "sara123", "sara@test.com"),
            "ali123": MockUser("Ali Karimi", "ali123", "ali@test.com")
        }
    def get_user(self, username):
        return self.users.get(username)

class MockSubscriptionManager:
    def get_member_status(self, username, current_date):
        if username == "reza123":
            return "Active", {"subscription_type": "One Month", "start_date": "2026-10-01", "end_date": "2026-11-01"}
        elif username == "ali123":
            return "Expired", {"subscription_type": "Three Months", "start_date": "2026-05-01", "end_date": "2026-08-01"}
        return "No Subscription", None

class MockExercise:
    def __init__(self, name, sets, reps, rest, desc):
        self.name = name
        self.sets = sets
        self.reps = reps
        self.rest_time = rest
        self.description = desc

class MockWorkoutPlan:
    def __init__(self, exercises):
        self.exercises = exercises

class MockWorkoutRepo:
    def get_plan_by_username(self, username):
        if username == "reza123":
            return MockWorkoutPlan([
                MockExercise("Bench Press", 3, 10, 60, "Keep back flat on the bench."),
                MockExercise("Squat", 4, 8, 90, "Go parallel, keep chest up.")
            ])
        return None

def run_demo():
    user_manager = MockUserManager()
    sub_manager = MockSubscriptionManager()
    workout_repo = MockWorkoutRepo()

    scenarios = ["reza123", "sara123", "ali123", "unknown_user"]

    for username in scenarios:
        print(f"\n\n>>> TESTING AUTHENTICATED MEMBER: '{username}' <<<")
        display_member_profile(username, user_manager, sub_manager)
        if user_manager.get_user(username):
            display_workout_plan(username, workout_repo)

if __name__ == "__main__":
    run_demo()
