from gym.data.errors import StorageError
from gym.data.transaction_repository import TransactionRepository
from menus.member_menu import _create_subscription_manager
from gym.data.class_repository import ClassRepository
from gym.manager.class_manager import ClassManager
from gym.manager.user_manager import UserManager
from menus.manager_menus.manage_users import manage_users_menu
from menus.manager_menus.manage_halls import manage_halls_menu
from menus.manager_menus.manage_classes import manage_classes_menu
from menus.manager_menus.manage_subscriptions import manage_subscriptions_menu
from menus.manager_menus.show_reports import show_reports


def manager_menu(user, user_storage, hall_manager, class_repository=None,
                 subscription_manager=None, payment_manager=None):
    if user.role != "Manager" or not user.is_active:
        print("Only an active Manager can enter this panel.")
        return
    user_manager = UserManager(user, user_storage)
    class_manager = None
    print("Welcome, " + user.name + " (" + user.username + ")")

    while True:
        print("--- Manager Panel ---")
        print("1. User Management")
        print("2. Hall Management")
        print("3. Classes Management")
        print("4. Subscription Management")
        print("5. Reports")
        print("6. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            manage_users_menu(user_manager)

        elif choice == "2":
            manage_halls_menu(hall_manager)

        elif choice == "3":
            if class_manager is None:
                repository = class_repository if class_repository is not None else ClassRepository()
                class_manager = _create_class_manager(repository, user_storage, hall_manager)
            manage_classes_menu(class_manager)

        elif choice == "4":
            try:
                if subscription_manager is None:
                    subscription_manager = _create_subscription_manager(user_storage)
                transactions = (payment_manager.transaction_repository if payment_manager is not None
                                else TransactionRepository())
                manage_subscriptions_menu(subscription_manager, transactions.load_all)
            except (OSError, ValueError, StorageError) as error:
                print("Could not open subscription management:", error)

        elif choice == "5":
            show_reports()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")


def _create_class_manager(repository, user_storage, hall_manager):
    def check_coach(username):
        users = user_storage.load_users()
        coach = user_storage.find_by_username(users, username)
        return coach is not None and coach.role == "Coach" and coach.is_active

    def check_hall(name):
        hall = hall_manager.get_hall(name)
        return hall is not None and hall.is_active

    return ClassManager(repository, check_coach, check_hall)
