"""Run the Issue 15 scenario with a separate demo-only JSON file."""
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from gym.auth_service import AuthService
from gym.data.errors import StorageError
from gym.data.user_storage import UserStorage


DEMO_FILE = Path(__file__).resolve().parent / "data" / "users_auth_fix_demo.json"


def show_result(title, result):
    print(title)
    print(result["message"])
    if result["success"]:
        user = result["user"]
        status = "Active" if user.is_active else "Inactive"
        print("Name:", user.name)
        print("Username:", user.username)
        print("Role:", user.role)
        print("Email:", user.email if user.email is not None else "Not provided")
        print("Account status:", status)
    print()


def main():
    storage = UserStorage(DEMO_FILE)
    try:
        storage.save_users([])
    except StorageError as error:
        print("Demo could not start:", error)
        return

    auth = AuthService(storage)

    show_result("1. Register active Manager manager01", auth.register_user(
        name="Gym Manager", username="manager01", password="Manager123@",
        role="Manager", email="manager@example.com", is_active=True,
    ))
    show_result("2. Register active Member reza123", auth.register_user(
        name="Reza", username="reza123", password="Reza123&",
        role="Member", email="reza@example.com", is_active=True,
    ))
    show_result("3. Register inactive Coach coach01", auth.register_user(
        name="Gym Coach", username="coach01", password="Coach123@",
        role="Coach", is_active=False,
    ))
    show_result("4. Reject duplicate username REZA123", auth.register_user(
        name="Another Member", username="REZA123", password="Member123@", role="Member",
    ))
    show_result("5. Reject password missing a digit", auth.register_user(
        name="Invalid Password", username="invalid_password", password="GymPassword@", role="Member",
    ))
    show_result("6. Reject invalid optional email", auth.register_user(
        name="Invalid Email", username="invalid_email", password="GymPass123@",
        role="Member", email="user@example",
    ))
    show_result("7. Log in Manager manager01", auth.login("manager01", "Manager123@"))
    show_result("8. Reject incorrect password", auth.login("reza123", "Wrong123@"))
    show_result("9. Reject inactive Coach coach01", auth.login("coach01", "Coach123@"))

    reloaded_auth = AuthService(UserStorage(DEMO_FILE))
    show_result("10. Reload data and log in Member reza123",
                reloaded_auth.login("reza123", "Reza123&"))


if __name__ == "__main__":
    main()
