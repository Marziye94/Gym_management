import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from gym.halls.hall_repository import HallRepository
from gym.halls.hall_service import HallManager
from gym.halls.hall_menu import manage_halls_menu, show_hall

DEMO_DATA_FILE = os.path.join(PROJECT_ROOT, "demos", "data", "halls_demo.json")


def reset_demo_data():
    if os.path.exists(DEMO_DATA_FILE):
        os.remove(DEMO_DATA_FILE)


def main():
    print("=== Hall Management Menu Demo ===")
    reset_demo_data()

    hall_repository = HallRepository(data_file=DEMO_DATA_FILE)
    hall_manager = HallManager(hall_repository)
    manage_halls_menu(hall_manager)

    print("\n--- Reloaded Hall Data ---")
    reloaded_repository = HallRepository(data_file=DEMO_DATA_FILE)
    halls = reloaded_repository.get_all()
    if not halls:
        print("No halls have been registered.")
    for hall in halls:
        show_hall(hall)
        print("-" * 30)

    print("\n=== Demo Completed ===")


main()