from menus.manager_menu import manager_menu
from menus.coach_menu import coach_menu
from menus.member_menu import member_menu


def main_menu():
    while True:
        print("--- Gym Management System ---")
        print("1. Manager")
        print("2. Coach")
        print("3. Member")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            manager_menu()
        elif choice == "2":
            coach_menu()
        elif choice == "3":
            member_menu()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
