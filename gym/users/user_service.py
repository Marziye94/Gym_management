from gym.users.auth_service import AuthService, auth_result
from gym.data.errors import StorageError
from gym.users.user_repository import UserStorage
from gym.users.user import User
from gym.users.user_validators import (
    validate_email,
    validate_name,
    validate_password,
    validate_username,
)


MANAGED_ROLES = ("Coach", "Member")


class UserManager:
    def __init__(self, manager_user, user_storage=None):
        self.manager_user = manager_user
        self.user_storage = user_storage if user_storage is not None else UserStorage()
        self.auth_service = AuthService(self.user_storage)

    def _is_manager(self):
        return (
            isinstance(self.manager_user, User)
            and self.manager_user.role == "Manager"
            and self.manager_user.is_active
        )

    def add_user(self, name, username, password, role, email=None, is_active=True):
        if not self._is_manager():
            return auth_result(False, "Only an active Manager can manage users.")
        if role not in MANAGED_ROLES:
            return auth_result(False, "Only Coach and Member accounts can be added.")

        return self.auth_service.register_user(
            name, username, password, role, email, is_active
        )

    def find_user(self, username):
        if not self._is_manager():
            return auth_result(False, "Only an active Manager can manage users.")

        username_result = validate_username(username)
        if not username_result["is_valid"]:
            return auth_result(False, username_result["message"])

        try:
            users = self.user_storage.load_users()
        except StorageError as error:
            return auth_result(False, "Could not find user: " + str(error))

        return self._find_managed_user(users, username)

    def edit_user(self, username, name, password, email=None, is_active=True):
        if not self._is_manager():
            return auth_result(False, "Only an active Manager can manage users.")

        username_result = validate_username(username)
        if not username_result["is_valid"]:
            return auth_result(False, username_result["message"])

        name_result = validate_name(name)
        if not name_result["is_valid"]:
            return auth_result(False, name_result["message"])

        password_result = validate_password(password)
        if not password_result["is_valid"]:
            return auth_result(False, password_result["message"])

        email_result = validate_email(email)
        if not email_result["is_valid"]:
            return auth_result(False, email_result["message"])

        if not isinstance(is_active, bool):
            return auth_result(False, "Account status must be a Boolean value.")

        try:
            users = self.user_storage.load_users()
            result = self._find_managed_user(users, username)
            if not result["success"]:
                return result

            user = result["user"]
            edited_user = User(
                user_id=user.user_id,
                name=name,
                username=user.username,
                password=password,
                role=user.role,
                is_active=is_active,
                email=email or None,
            )
            users[users.index(user)] = edited_user
            self.user_storage.save_users(users)
        except StorageError as error:
            return auth_result(False, "User update failed: " + str(error))

        return auth_result(True, "User updated successfully.", edited_user)

    def list_users(self):
        if not self._is_manager():
            return {
                "success": False,
                "message": "Only an active Manager can manage users.",
                "users": [],
            }

        try:
            users = self.user_storage.load_users()
        except StorageError as error:
            return {
                "success": False,
                "message": "Could not load users: " + str(error),
                "users": [],
            }

        managed_users = []
        for user in users:
            if user.role in MANAGED_ROLES:
                managed_users.append(user)
        return {
            "success": True,
            "message": "Users loaded successfully.",
            "users": managed_users,
        }

    def set_active(self, username, is_active):
        if not self._is_manager():
            return auth_result(False, "Only an active Manager can manage users.")
        if not isinstance(is_active, bool):
            return auth_result(False, "Account status must be a Boolean value.")

        username_result = validate_username(username)
        if not username_result["is_valid"]:
            return auth_result(False, username_result["message"])

        try:
            users = self.user_storage.load_users()
            result = self._find_managed_user(users, username)
            if not result["success"]:
                return result

            user = result["user"]
            if is_active:
                user.activate()
            else:
                user.deactivate()
            self.user_storage.save_users(users)
        except StorageError as error:
            return auth_result(False, "Account status update failed: " + str(error))

        return auth_result(True, "Account status updated successfully.", user)

    def _find_managed_user(self, users, username):
        user = self.user_storage.find_by_username(users, username)
        if user is None:
            return auth_result(False, "User not found.")
        if user.role not in MANAGED_ROLES:
            return auth_result(False, "Only Coach and Member accounts can be managed.")
        return auth_result(True, "User found.", user)
