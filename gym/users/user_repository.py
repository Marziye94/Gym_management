import json
import os

from gym.data.errors import InvalidUserDataError, StorageError
from gym.users.user import ALLOWED_ROLES, User
from gym.users.user_validators import (
    validate_email,
    validate_name,
    validate_password,
    validate_username,
)


REQUIRED_USER_FIELDS = (
    "user_id",
    "name",
    "username",
    "password",
    "role",
    "is_active",
)


class UserStorage:
    def __init__(self, data_file=None):
        if data_file is None:
            data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "users.json"))
        self.data_file = os.fspath(data_file)

    def load_users(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                records = json.load(file)
        except FileNotFoundError:
            return []
        except (ValueError, UnicodeError):
            raise InvalidUserDataError("User data file contains invalid JSON or encoding.")
        except OSError:
            raise StorageError("User data file could not be read.")

        if not isinstance(records, list):
            raise InvalidUserDataError("User data file must contain a list.")

        users = []
        for record in records:
            users.append(self.user_from_dict(record))

        self.validate_unique_users(users)
        return users

    def save_users(self, users):
        if not isinstance(users, list):
            raise InvalidUserDataError("Users must be provided as a list.")

        records = []
        for user in users:
            records.append(self.user_to_dict(user))

        self.validate_unique_users(users)
        content = json.dumps(records, indent=2)
        self._write_file(content)

    def find_by_username(self, users, username):
        if not isinstance(username, str):
            return None

        for user in users:
            if user.username.casefold() == username.casefold():
                return user
        return None

    def get_user(self, username):
        return self.find_by_username(self.load_users(), username)

    def get_next_user_id(self, users):
        biggest_id = 0
        for user in users:
            if user.user_id > biggest_id:
                biggest_id = user.user_id
        return biggest_id + 1

    def user_from_dict(self, record):
        self._validate_record(record)
        return User(
            user_id=record["user_id"],
            name=record["name"],
            username=record["username"],
            password=record["password"],
            role=record["role"],
            is_active=record["is_active"],
            email=record.get("email"),
        )

    def user_to_dict(self, user):
        if not isinstance(user, User):
            raise InvalidUserDataError("Only User objects can be saved.")

        try:
            record = {
                "user_id": user.user_id,
                "name": user.name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "is_active": user.is_active,
                "email": user.email,
            }
        except AttributeError:
            raise InvalidUserDataError("A user object is incomplete.")

        self._validate_record(record)
        return record

    def _validate_record(self, record):
        if not isinstance(record, dict):
            raise InvalidUserDataError("A stored user record must be a dictionary.")

        for field in REQUIRED_USER_FIELDS:
            if field not in record:
                raise InvalidUserDataError("A stored user record is incomplete: " + field + ".")

        if type(record["user_id"]) is not int or record["user_id"] < 1:
            raise InvalidUserDataError("A stored user has an invalid user ID.")

        if record["role"] not in ALLOWED_ROLES:
            raise InvalidUserDataError("A stored user has an invalid role.")

        if not isinstance(record["is_active"], bool):
            raise InvalidUserDataError("A stored user has an invalid account status.")

        name_result = validate_name(record["name"])
        self._check_validation(name_result)

        username_result = validate_username(record["username"])
        self._check_validation(username_result)

        password_result = validate_password(record["password"])
        self._check_validation(password_result)

        email_result = validate_email(record.get("email"))
        self._check_validation(email_result)

    def _check_validation(self, result):
        if not result["is_valid"]:
            raise InvalidUserDataError("Invalid stored user: " + result["message"])

    def validate_unique_users(self, users):
        seen_ids = set()
        seen_usernames = set()

        for user in users:
            if user.user_id in seen_ids:
                raise InvalidUserDataError("Stored users contain duplicate user IDs.")

            username = user.username.casefold()
            if username in seen_usernames:
                raise InvalidUserDataError("Stored users contain duplicate usernames.")

            seen_ids.add(user.user_id)
            seen_usernames.add(username)

    def _write_file(self, content):
        directory = os.path.dirname(os.path.abspath(self.data_file))
        try:
            os.makedirs(directory, exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as file:
                file.write(content)
        except OSError:
            raise StorageError("User data file could not be written.")
