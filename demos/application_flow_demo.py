"""Open the real application using only demos/data/application files."""
from datetime import date
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from gym.data.errors import StorageError
from main import create_application
from menus.main_menu import main_menu

DATA_DIRECTORY = PROJECT_ROOT / "demos" / "data" / "application"


def prepare_demo(application):
    # Do not seed or overwrite data if a repository could not be loaded.
    if any(value is None for value in application.values()):
        print("Demo data is unavailable. Fix its files before running the scenario.")
        return False
    auth = application["auth"]
    users = application["user_storage"]
    for name, username, password, role in (
        ("Demo Manager", "manager01", "Manager123@", "Manager"),
        ("Demo Coach", "coach01", "Coach123@", "Coach"),
        ("Reza", "reza123", "Member123@", "Member"),
    ):
        if users.get_user(username) is None:
            result = auth.register_user(name, username, password, role)
            if not result["success"]:
                print(result["message"])
                return False
    halls = application["hall_manager"]
    if halls.get_hall("Main Hall") is None:
        result = halls.create_hall("Main Hall", 20, ["Mat"])
        if not result.success:
            print(result.message)
            return False
    classes = application["class_manager"]
    if application["class_repository"].get_class("Yoga") is None:
        result = classes.create_class("Yoga", "Yoga", "coach01", "Main Hall", "Monday", "18:00", 10)
        if not result.success:
            print(result.message)
            return False
    subscriptions = application["subscription_manager"]
    if not subscriptions.get_member_subscriptions("reza123"):
        result = subscriptions.register_subscription("reza123", "One Month", 5000, 30, date.today())
        if not result.success:
            print(result.message)
            return False
    enrollments = application["enrollment_repository"]
    if not enrollments.get_by_member_username("reza123"):
        success, message = application["enrollment_manager"].register_member("reza123", "Yoga")
        if not success:
            print(message)
            return False
    wallets = application["wallet_repository"]
    if "reza123" not in wallets.wallets:
        success, message = application["payment_manager"].charge_wallet(
            "reza123", "1234567890123456", 12, 1408, "123456", "123", 10000)
        if not success:
            print(message)
            return False
    return True


def main():
    application = create_application(DATA_DIRECTORY)
    try:
        if not prepare_demo(application):
            print("Demo setup could not be completed.")
            return
    except (OSError, ValueError, StorageError) as error:
        print("Demo setup could not be completed:", error)
        return
    print("=== Application Flow Demo ===")
    print("All data is under demos/data/application/. Existing demo data is preserved.")
    print("Manager: manager01 / Manager123@")
    print("Coach: coach01 / Coach123@")
    print("Member: reza123 / Member123@")
    print("Follow this scenario:")
    print("1. Start: 1; manager01; Manager123@; Manager: 1; Users: 3, 5; Manager: 6.")
    print("2. Start: 2; reza123; Member123@; role rejected; choose 2 to go back.")
    print("3. Start: 2; coach01; Coach123@; Coach: 1, 3.")
    print("4. Start: 3; reza123; Member123@; Member: 1, 2; Wallet: 1, 5; Member: 5.")
    print("5. Start: 4 to exit and reload the same demo files.")
    main_menu(application)
    print("\n--- Recreate Dependencies and Reload Demo Data ---")
    reloaded = create_application(DATA_DIRECTORY)
    if any(value is None for value in reloaded.values()):
        print("Saved demo data could not be reloaded. Its files were preserved.")
        return
    member = reloaded["user_storage"].get_user("reza123")
    gym_class = reloaded["class_repository"].get_class("Yoga")
    print("Saved Member:", member.username if member is not None else "Not found")
    print("Saved class:", gym_class.name if gym_class is not None else "Not found")
    status, info = reloaded["subscription_manager"].get_member_status("reza123", date.today())
    print("Saved subscription:", status, info)
    print("Saved registrations:", len(reloaded["enrollment_repository"].get_by_member_username("reza123")))
    print("Saved wallet balance:", reloaded["payment_manager"].get_balance("reza123"))


if __name__ == "__main__":
    main()
