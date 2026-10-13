from gym.data.hall_repository import HallRepository
from gym.manager.hall_manager import HallManager
from menus.manager_menu import manager_menu
from menus.coach_menu import coach_menu
from menus.member_menu import member_menu


def main_menu():
    hall_repository = HallRepository()
    hall_manager = HallManager(hall_repository)

    while True:
        print("--- Gym Management System ---")
        print("1. Manager")
        print("2. Coach")
        print("3. Member")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            manager_menu(hall_manager)
        elif choice == "2":
            coach_menu()
        elif choice == "3":
            member_menu()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")