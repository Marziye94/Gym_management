from gym.data.errors import StorageError
from menus.member_menus.profile import display_member_profile
from menus.member_menus.view_workout_plan import display_workout_plan
from menus.member_menus.wallet_menu import wallet_menu
from menus.member_menus.manage_classes import manage_classes_menu


def member_menu(user, application):
    if user.role != "Member" or not user.is_active:
        print("Only an active Member can enter this panel.")
        return
    print("Welcome, " + user.name + " (" + user.username + ")")
    while True:
        print("--- Member Panel ---")
        print("1. Profile and Subscription Status")
        print("2. Wallet")
        print("3. Classes")
        print("4. Workout Plan")
        print("5. Logout")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                if application["subscription_manager"] is None:
                    print("Profile and subscription information is unavailable.")
                    continue
                display_member_profile(user.username, application["user_storage"],
                                       application["subscription_manager"])
            elif choice == "2":
                if application["payment_manager"] is None or application["subscription_manager"] is None:
                    print("Wallet features are unavailable.")
                    continue
                wallet_menu(user.username, application["payment_manager"], application["subscription_manager"])
            elif choice == "3":
                if application["enrollment_manager"] is None:
                    print("Class enrollment is unavailable.")
                    continue
                manage_classes_menu(user.username, application["class_repository"], application["enrollment_manager"])
            elif choice == "4":
                if application["workout_repository"] is None:
                    print("Workout plans are unavailable.")
                    continue
                display_workout_plan(user.username, application["workout_repository"])
            elif choice == "5":
                return
            else:
                print("Invalid choice. Please try again.")
        except (OSError, ValueError, StorageError) as error:
            print("Could not open or complete this feature:", error)
