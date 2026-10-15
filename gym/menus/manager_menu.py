from gym.errors import StorageError
from gym.users.user_menu import manage_users_menu
from gym.halls.hall_menu import manage_halls_menu
from gym.classes.class_menu import manage_classes_menu
from gym.subscriptions.subscription_menu import manage_subscriptions_menu
from gym.reports.report_menu import show_reports


def manager_menu(user, application):
    if user.role != "Manager" or not user.is_active:
        print("Only an active Manager can enter this panel.")
        return
    print("Welcome, " + user.name + " (" + user.username + ")")
    while True:
        print("--- Manager Panel ---")
        print("1. User Management")
        print("2. Hall Management")
        print("3. Classes Management")
        print("4. Subscription and Payment Management")
        print("5. Reports")
        print("6. Logout")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                manage_users_menu(application["user_manager"])
            elif choice == "2":
                if application["hall_manager"] is None:
                    print("Hall management is unavailable.")
                    continue
                manage_halls_menu(application["hall_manager"])
            elif choice == "3":
                if application["class_manager"] is None or application["enrollment_manager"] is None:
                    print("Class management is unavailable.")
                    continue
                manage_classes_menu(application["class_manager"],application["enrollment_manager"])
            elif choice == "4":
                if application["subscription_manager"] is None or application["transaction_repository"] is None:
                    print("Subscription and payment management is unavailable.")
                    continue
                manage_subscriptions_menu(application["subscription_manager"],application["transaction_repository"].load_all)
            elif choice == "5":
                if application["report_manager"] is None:
                    print("Reports are unavailable.")
                    continue
                show_reports(application["report_manager"])
            elif choice == "6":
                return
            else:
                print("Invalid choice. Please try again.")
        except (OSError, ValueError, StorageError) as error:
            print("Could not open or complete this feature:", error)
