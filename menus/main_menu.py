from getpass import getpass

from gym.auth_service import AuthService
from gym.data.hall_repository import HallRepository
from gym.data.user_storage import UserStorage
from gym.manager.hall_manager import HallManager
from menus.manager_menu import manager_menu
from menus.coach_menu import coach_menu
from menus.member_menu import member_menu


def main_menu(user_storage=None, hall_repository=None):
    storage = user_storage if user_storage is not None else UserStorage()
    halls = hall_repository if hall_repository is not None else HallRepository()
    auth = AuthService(storage)
    hall_manager = HallManager(halls)
    try:
        _start_menu(auth, storage, hall_manager)
    except (EOFError, KeyboardInterrupt):
        print("\nProgram closed.")


def _start_menu(auth, storage, hall_manager):
    while True:
        print("--- Gym Management System ---")
        print("1. Manager Login")
        print("2. Coach Login")
        print("3. Member Login")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            user = _login(auth, "Manager")
            if user is not None:
                manager_menu(user, storage, hall_manager)
        elif choice == "2":
            user = _login(auth, "Coach")
            if user is not None:
                coach_menu(user, storage)
        elif choice == "3":
            user = _login(auth, "Member")
            if user is not None:
                member_menu(user, storage)
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")


def _login(auth, expected_role):
    while True:
        print("--- " + expected_role + " Login ---")
        username = input("Username: ")
        password = getpass("Password: ")
        result = auth.login(username, password)

        if result["success"]:
            user = result["user"]
            if user.role == expected_role:
                print(result["message"])
                return user
            print("This account cannot enter the " + expected_role + " panel.")
        else:
            print(result["message"])

        while True:
            print("1. Retry")
            print("2. Back to Start menu")
            choice = input("Choose an option: ").strip()
            if choice == "1":
                break
            if choice == "2":
                return None
            print("Invalid choice. Please try again.")
