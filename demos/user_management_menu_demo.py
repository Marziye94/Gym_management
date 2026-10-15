"""Open the real menus with a separate demo user file."""
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from gym.data.errors import StorageError
from main import create_application
from menus.main_menu import main_menu
from menus.manager_menus.manage_users import display_user


DATA_DIRECTORY = PROJECT_ROOT / "demos" / "data" / "user_management"



def main():
    application = create_application(DATA_DIRECTORY)
    storage = application["user_storage"]
    try:
        storage.save_users([])
    except StorageError as error:
        print("Demo could not start:", error)
        return

    auth = application["auth"]
    result = auth.register_user(
        name="Main Manager",
        username="manager01",
        password="Manager123@",
        role="Manager",
    )
    if not result["success"]:
        print(result["message"])
        return

    print("Demo ready. Log in using the predefined Manager account.")
    main_menu(application)

    reloaded = create_application(DATA_DIRECTORY)
    reloaded_storage = reloaded["user_storage"]
    result = reloaded["auth"].login("manager01", "Manager123@")
    if not result["success"]:
        print("Demo reload failed:", result["message"])
        return

    try:
        users = reloaded_storage.load_users()
    except StorageError as error:
        print("Demo reload failed:", error)
        return

    print("--- Reloaded Users ---")
    for user in users:
        display_user(user)


if __name__ == "__main__":
    main()
