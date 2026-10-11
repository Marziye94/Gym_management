from menus.manger_menus.manage_users import manage_users_menu
from menus.manger_menus.manage_halls import manage_halls_menu
from menus.manger_menus.manage_classes import manage_classes_menu
from menus.manger_menus.manage_subscriptions import manage_subscriptions_menu
from menus.manger_menus.show_reports import show_reports


def manager_menu():

    while True:
        print("--- Manager Panel ---")
        print("1. User Management")
        print("2. Hall Management")
        print("3. Classes Management")
        print("4. Subscription Management")
        print("5. Reports")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            manage_users_menu()

        elif choice == "2":
            manage_halls_menu()

        elif choice == "3":
            manage_classes_menu()

        elif choice == "4":
            manage_subscriptions_menu()

        elif choice == "5":
            show_reports()

        elif choice == "6":
            break

        print("Invalid choice. Please try again.")
