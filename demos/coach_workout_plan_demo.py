import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from gym.manager.workout_plan_manager import WorkoutPlanManager
from gym.data.class_repository import ClassRepository
from gym.data.errors import StorageError
from gym.data.hall_repository import HallRepository
from gym.data.user_storage import UserStorage
from gym.data.workout_plan_repository import WorkoutPlanRepository
from gym.manager.hall_manager import HallManager
from gym.models.gym_class import GymClass
from gym.models.user import User
from menus.coach_menus.manage_workouts import show_plan
from menus.coach_menus.view_classes import view_my_classes_menu

DEMO_DATA_FOLDER = os.path.join(PROJECT_ROOT, "demos", "data")
PLANS_FILE = os.path.join(DEMO_DATA_FOLDER, "workout_plans_demo.json")
USERS_FILE = os.path.join(DEMO_DATA_FOLDER, "coach_demo_users.json")
HALLS_FILE = os.path.join(DEMO_DATA_FOLDER, "coach_demo_halls.json")
CLASSES_FILE = os.path.join(DEMO_DATA_FOLDER, "coach_demo_classes.json")


class DemoEnrollmentLookup:
    def __init__(self, active_enrollments):
        self.active_enrollments = active_enrollments

    def get_active_member_usernames(self, class_name):
        return self.active_enrollments.get(class_name, [])


def reset_demo_data():
    os.makedirs(DEMO_DATA_FOLDER, exist_ok=True)
    for path in (PLANS_FILE, USERS_FILE, HALLS_FILE, CLASSES_FILE):
        if os.path.exists(path):
            os.remove(path)


def create_demo_users():
    user_storage = UserStorage()
    user_storage.data_file = USERS_FILE
    users = [
        User(user_id=1, name="Coach One", username="coach01", password="Coach01@pass", role="Coach"),
        User(user_id=2, name="Coach Two", username="coach02", password="Coach02@pass", role="Coach"),
        User(user_id=3, name="Reza", username="reza123", password="Reza123@pass", role="Member"),
        User(user_id=4, name="Sara", username="sara123", password="Sara123@pass", role="Member"),
    ]
    try:
        user_storage.save_users(users)
    except StorageError as error:
        print("Demo users could not be saved: " + str(error))
        return None
    return user_storage

def create_demo_classes():
    hall_manager = HallManager(HallRepository(data_file=HALLS_FILE))
    hall_manager.create_hall("Main Hall", 20, ["Mat"])
    hall_manager.create_hall("Strength Hall", 15, ["Bench"])

    class_repository = ClassRepository(data_file=CLASSES_FILE)
    class_repository.add(GymClass("Yoga", "Yoga", "coach01", "Main Hall", "Monday", "18:00", 10, 9))
    class_repository.add(GymClass("Boxing", "Boxing", "coach02", "Strength Hall", "Tuesday", "19:00", 8, 8))
    return class_repository


def show_exercise(plan, number):
    exercise = plan.get_exercise(number)
    print(f"{number}. {exercise.name} | Sets: {exercise.sets} | Repetitions: {exercise.repetitions} "
          f"| Rest: {exercise.rest_time} seconds | Description: {exercise.description}")


def main():
    print("=== Coach Workout Plan Demo ===")
    reset_demo_data()

    user_storage = create_demo_users()
    if user_storage is None:
        return
    class_repository = create_demo_classes()
    enrollment_lookup = DemoEnrollmentLookup({"Yoga": ["reza123"], "Boxing": []})
    plan_repository = WorkoutPlanRepository(data_file=PLANS_FILE)
    manager = WorkoutPlanManager(plan_repository, class_repository, enrollment_lookup)

    try:
        coach = user_storage.find_by_username(user_storage.load_users(), "coach01")
    except StorageError as error:
        print(error)
        return
    print(f"Authenticated coach: {coach.username}")

    print("\n--- Step 1: coach01 classes ---")
    view_my_classes_menu(coach, manager)

    print("\n--- Step 2: Select Yoga and reza123 ---")
    print(manager.check_member(coach, "Yoga", "reza123").message)

    print("\n--- Step 3: Create a plan with two exercises ---")
    print(manager.create_plan(coach, "Yoga", "reza123").message)
    print(manager.add_exercise(coach, "Yoga", "reza123", "Sun Salutation", 3, 10, 30, "Slow breathing").message)
    print(manager.add_exercise(coach, "Yoga", "reza123", "Plank", 2, 1, 45, "Hold for 30 seconds").message)
    plan = manager.get_plan(coach, "Yoga", "reza123").data
    show_plan(plan)

    print("\n--- Step 4: Edit exercise 1 ---")
    result = manager.update_exercise(coach, "Yoga", "reza123", 1, "Sun Salutation", 4, 12, 30, "Slow breathing")
    print(result.message)
    show_exercise(plan, 1)

    print("\n--- Step 5: Invalid edit (sets 0, repetitions -5) ---")
    result = manager.update_exercise(coach, "Yoga", "reza123", 1, "Sun Salutation", 0, -5, 30, "Slow breathing")
    print(result.message)
    print("Exercise after the failed edit:")
    show_exercise(plan, 1)

    print("\n--- Step 6: Create a plan for sara123 ---")
    print(manager.create_plan(coach, "Yoga", "sara123").message)

    print("\n--- Step 7: Access coach02 class ---")
    print(manager.get_coach_class(coach, "Boxing").message)
    print(manager.create_plan(coach, "Boxing", "reza123").message)

    print("\n--- Step 8: Reload and display the saved plan ---")
    reloaded_repository = WorkoutPlanRepository(data_file=PLANS_FILE)
    saved_plan = reloaded_repository.find("coach01", "Yoga", "reza123")
    if saved_plan is None:
        print("The saved plan was not found.")
    else:
        show_plan(saved_plan)

    print("\n=== Demo Completed ===")


main()