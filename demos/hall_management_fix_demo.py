import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from gym.halls.hall_repository import HallRepository
from gym.halls.hall_service import HallManager


def show_hall(hall):
    print(f"Name: {hall.name}")
    print(f"Capacity: {hall.capacity}")
    print(f"Equipment: {', '.join(hall.equipment)}")
    print(f"Status: {'Active' if hall.is_active else 'Inactive'}")


def main():
    demo_data_file = os.path.join(PROJECT_ROOT, "demos", "data", "halls_fix_demo.json")
    if os.path.exists(demo_data_file):
        os.remove(demo_data_file)
    hall_manager = HallManager(HallRepository(data_file=demo_data_file))

    hall_name = "Main Hall"
    capacity = 20
    equipment = ["Treadmill", "Dumbbell"]
    is_active = False

    print("=== Hall Management Fix Demo ===")

    print("\n--- Created Hall ---")
    result = hall_manager.create_hall(hall_name, capacity, equipment, is_active)
    if result.success:
        show_hall(result.data)
    else:
        print(result.message)

    print("\n--- Updated Hall ---")
    result = hall_manager.update_hall("Main Hall", "Strength Hall", 30, ["Dumbbell", "Bench"])
    if result.success:
        show_hall(result.data)
    else:
        print(result.message)

    print("\n--- Lookup Using Old Name ---")
    if hall_manager.get_hall("Main Hall") is None:
        print("Main Hall was not found.")
    else:
        print("Main Hall was found.")

    print("\n--- Lookup Using New Name ---")
    hall = hall_manager.get_hall("Strength Hall")
    if hall is None:
        print("Strength Hall was not found.")
    else:
        print("Strength Hall was found.")
        show_hall(hall)

    print("\n--- Invalid Update ---")
    result = hall_manager.update_hall("Strength Hall", "Invalid Hall", -10, ["Bench"])
    print(result.message)

    print("\n--- Final Hall Information ---")
    show_hall(hall_manager.get_hall("Strength Hall"))

    print("\n=== Demo Completed ===")


main()