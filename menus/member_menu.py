from menus.member_menus.wallet_menu import wallet_menu
from gym.data.subscription_repository import SubscriptionRepository
from gym.data.transaction_repository import TransactionRepository
from gym.data.wallet_repository import WalletRepository
from gym.financial.Bank import API
from gym.manager.payment_manager import PaymentManager
from gym.manager.subscription_manager import SubscriptionManager


def member_menu(user, user_storage, payment_manager=None, subscription_manager=None):
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

        choice = input("choose an option: ")

        if choice == "1":
            pass
        elif choice == "2":
            try:
                if payment_manager is None:
                    payment_manager = PaymentManager(WalletRepository(), TransactionRepository(), API())
                if subscription_manager is None:
                    subscription_manager = _create_subscription_manager(user_storage)
            except (OSError, ValueError) as error:
                print("Could not open wallet:", error)
                continue
            wallet_menu(user.username, payment_manager, subscription_manager)
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def _create_subscription_manager(user_storage, repository=None):
    def is_member_active(username):
        users = user_storage.load_users()
        member = user_storage.find_by_username(users, username)
        return member is not None and member.role == "Member" and member.is_active

    subscriptions = repository if repository is not None else SubscriptionRepository()
    return SubscriptionManager(subscriptions, is_member_active)
