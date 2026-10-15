import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from gym.classes.class_repository import ClassRepository
from gym.classes.class_service import ClassManager
from gym.classes.class_menu import manage_classes_menu

def run_menu_demo():
    demo_file = os.path.join(PROJECT_ROOT, "demos", "data", "classes_demo.json")


    os.makedirs(os.path.dirname(demo_file), exist_ok=True)
    with open(demo_file, "w", encoding="utf-8") as f:
        f.write("[]")

    coaches = {
        "Sara": True,
        "Reza": True,
        "Inactive Coach": False,
    }

    halls = {
        "Main Hall": True,
        "Studio Hall": True,
        "Inactive Hall": False,
    }

    def check_coach(name):
        return coaches.get(name, False)

    def check_hall(name):
        return halls.get(name, False)


    repo = ClassRepository(data_file=demo_file)
    manager = ClassManager(repo, check_coach, check_hall)
    manage_classes_menu(manager)

    reloaded_repo = ClassRepository(data_file=demo_file)
    saved_classes = reloaded_repo.get_all()

    print("\n--- Reloaded Class Data ---\n")
    if len(saved_classes) == 0:
        print("No classes have been registered.")
    else:
        for gym_class in saved_classes:
            status = "Active" if gym_class.is_active else "Inactive"
            print(f"Title: {gym_class.name}")
            print(f"Sport Type: {gym_class.exercise}")
            print(f"Coach: {gym_class.coach_name}")
            print(f"Hall: {gym_class.hall_name}")
            print(f"Day: {gym_class.day}")
            print(f"Time: {gym_class.time}")
            print(f"Total Capacity: {gym_class.capacity}")
            print(f"Remaining Capacity: {gym_class.remaining_capacity}")
            print(f"Status: {status}")

if __name__ == "__main__":
    run_menu_demo()
