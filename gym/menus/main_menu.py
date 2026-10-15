from getpass import getpass

from gym.menus.manager_menu import manager_menu
from gym.menus.coach_menu import coach_menu
from gym.menus.member_menu import member_menu


def main_menu(application):
    try:
        _start_menu(application)
    except (EOFError, KeyboardInterrupt):
        print("\nProgram closed.")


def _start_menu(application):
    while True:
        print("--- Gym Management System ---")
        print("1. Manager Login")
        print("2. Coach Login")
        print("3. Member Login")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            user = _login(application["auth"], "Manager")
            if user is not None:
                application["user_manager"].manager_user = user
                try:
                    manager_menu(user, application)
                finally:
                    application["user_manager"].manager_user = None
        elif choice == "2":
            user = _login(application["auth"], "Coach")
            if user is not None:
                coach_menu(user, application)
        elif choice == "3":
            user = _login(application["auth"], "Member")
            if user is not None:
                member_menu(user, application)
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")


def _login(auth, expected_role):
    if auth is None:
        print("Login is unavailable because user data could not be loaded.")
        return None
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
