"""Open the real menus with a separate demo user file."""
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from gym.auth_service import AuthService
from gym.data.class_repository import ClassRepository
from gym.data.errors import StorageError
from gym.data.hall_repository import HallRepository
from gym.data.user_storage import UserStorage
from menus.main_menu import main_menu
from menus.manager_menus.manage_users import display_user


DEMO_FILE = Path(__file__).resolve().parent / "data" / "users_menu_demo.json"


def main():
    storage = UserStorage(DEMO_FILE)
    try:
        storage.save_users([])
    except StorageError as error:
        print("Demo could not start:", error)
        return

    auth = AuthService(storage)
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
    halls = HallRepository(DEMO_FILE.with_name("halls_user_menu_demo.json"))
    classes = ClassRepository(DEMO_FILE.with_name("classes_user_menu_demo.json"))
    main_menu(storage, halls, classes)

    reloaded_storage = UserStorage(DEMO_FILE)
    reloaded_auth = AuthService(reloaded_storage)
    result = reloaded_auth.login("manager01", "Manager123@")
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
