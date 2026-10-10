import json
import os

from gym.data.errors import InvalidUserDataError, StorageError
from gym.models.user import ALLOWED_ROLES, User


REQUIRED_USER_FIELDS = (
    "user_id",
    "username",
    "password",
    "role",
    "is_active",
)


class UserStorage:
    def __init__(self):
        current_directory = os.path.dirname(__file__)
        self.data_file = os.path.join(current_directory, "users.json")

    def load_users(self):
        if not os.path.exists(self.data_file):
            return []

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                stored_users = json.load(file)
        except json.JSONDecodeError:
            raise InvalidUserDataError("User data file contains invalid JSON.")
        except OSError:
            raise StorageError("User data file could not be read.")

        if not isinstance(stored_users, list):
            raise InvalidUserDataError("User data file must contain a list.")

        users = []

        for stored_user in stored_users:
            users.append(self.user_from_dict(stored_user))

        return users

    def save_users(self, users):
        stored_users = []

        for user in users:
            stored_users.append(self.user_to_dict(user))

        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(stored_users, file, ensure_ascii=False, indent=2)
        except OSError:
            raise StorageError("User data file could not be written.")

    def user_from_dict(self, stored_user):
        if not isinstance(stored_user, dict):
            raise InvalidUserDataError(
                "A stored user record must be a dictionary."
            )

        for field in REQUIRED_USER_FIELDS:
            if field not in stored_user:
                raise InvalidUserDataError("A stored user record is incomplete.")

        if stored_user["role"] not in ALLOWED_ROLES:
            raise InvalidUserDataError("A stored user has an invalid role.")

        if not isinstance(stored_user["user_id"], int):
            raise InvalidUserDataError("A stored user has an invalid user ID.")

        if not isinstance(stored_user["username"], str):
            raise InvalidUserDataError("A stored user has an invalid username.")

        if not isinstance(stored_user["password"], str):
            raise InvalidUserDataError("A stored user has an invalid password.")

        if not isinstance(stored_user["is_active"], bool):
            raise InvalidUserDataError(
                "A stored user has an invalid account status."
            )

        email = stored_user.get("email")
        if email is not None and not isinstance(email, str):
            raise InvalidUserDataError("A stored user has an invalid email.")

        return User(
            stored_user["user_id"],
            stored_user["username"],
            stored_user["password"],
            stored_user["role"],
            stored_user["is_active"],
            email,
        )

    def user_to_dict(self, user):
        return {
            "user_id": user.user_id,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "is_active": user.is_active,
            "email": user.email,
        }

    def find_by_username(self, users, username):
        for user in users:
            if user.username.lower() == username.lower():
                return user

        return None

    def get_next_user_id(self, users):
        biggest_id = 0

        for user in users:
            if isinstance(user.user_id, int) and user.user_id > biggest_id:
                biggest_id = user.user_id

        return biggest_id + 1
