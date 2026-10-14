from datetime import date, timedelta
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from main import create_application
from gym.workouts.workout_plan import Exercise, WorkoutPlan
from gym.users.member_profile_menu import display_member_profile
from gym.workouts.member_workout_menu import display_workout_plan


def run_demo():
    application = create_application(PROJECT_ROOT / "demos" / "data" / "member_profile")
    users = application["user_storage"]
    auth = application["auth"]
    subscriptions = application["subscription_manager"]
    workouts = application["workout_repository"]
    for name, username in (("Reza", "reza123"), ("Sara", "sara123"), ("Ali", "ali123")):
        if users.get_user(username) is None:
            result = auth.register_user(name, username, "Member123@", "Member")
            if not result["success"]:
                print(result["message"])
                return
    for username, start_date in (("reza123", date.today()), ("ali123", date.today() - timedelta(days=60))):
        if not subscriptions.get_member_subscriptions(username):
            result = subscriptions.register_subscription(username, "One Month", 5000, 30, start_date)
            if not result.success:
                print(result.message)
                return
    if not workouts.get_by_member_username("reza123"):
        plan = WorkoutPlan(workouts.generate_id(), "coach01", "Yoga", "reza123", [
            Exercise("Bench Press", 3, 10, 60, "Keep back flat on the bench."),
            Exercise("Squat", 4, 8, 90, "Keep chest up."),
        ])
        workouts.add(plan)
    for username in ("reza123", "sara123", "ali123", "unknown_user"):
        print("\nAuthenticated Member:", username)
        display_member_profile(username, users, subscriptions)
        if users.get_user(username) is not None:
            display_workout_plan(username, workouts)


if __name__ == "__main__":
    run_demo()
