from gym.errors import StorageError
from gym.users.user_repository import UserStorage
from gym.users.user import ALLOWED_ROLES, User
from gym.users.user_validators import validate_email, validate_name, validate_password, validate_username


def auth_result(success, message, user=None):
    return {
        "success": success,
        "message": message,
        "user": user,
    }


class AuthService:
    def __init__(self, user_storage=None):
        self.user_storage = user_storage if user_storage is not None else UserStorage()

    def register_user(self, name, username, password, role, email=None, is_active=True):
        if isinstance(username, str):
            username = username.strip()

        name_result = validate_name(name)
        if not name_result["is_valid"]:
            return auth_result(False, name_result["message"])

        username_result = validate_username(username)
        if not username_result["is_valid"]:
            return auth_result(False, username_result["message"])

        password_result = validate_password(password)
        if not password_result["is_valid"]:
            return auth_result(False, password_result["message"])

        email_result = validate_email(email)
        if not email_result["is_valid"]:
            return auth_result(False, email_result["message"])

        if not isinstance(role, str) or role not in ALLOWED_ROLES:
            message = "Role must be Manager, Coach, or Member."
            return auth_result(False, message)

        if not isinstance(is_active, bool):
            return auth_result(False, "Account status must be a Boolean value.")

        try:
            users = self.user_storage.load_users()
        except StorageError as error:
            return auth_result(False, "Registration failed: " + str(error))

        saved_user = self.user_storage.find_by_username(users, username)
        if saved_user is not None:
            return auth_result(False, "Username already exists.")

        if email == "":
            email = None

        user_id = self.user_storage.get_next_user_id(users)
        user = User(user_id, name, username, password, role, is_active, email)
        users.append(user)

        try:
            self.user_storage.save_users(users)
        except StorageError as error:
            return auth_result(False, "Registration failed: " + str(error))

        return auth_result(True, "Registration successful.", user)

    def login(self, username, password):
        if not isinstance(username, str) or not isinstance(password, str):
            return auth_result(False, "Invalid username or password.")
        username = username.strip()
        if not username or not password.strip():
            return auth_result(False, "Invalid username or password.")

        try:
            users = self.user_storage.load_users()
        except StorageError as error:
            return auth_result(False, "Login failed: " + str(error))

        user = self.user_storage.find_by_username(users, username)

        if user is None or user.password != password:
            return auth_result(False, "Invalid username or password.")

        if not user.is_active:
            return auth_result(False, "Login failed: account is inactive.")

        return auth_result(True, "Login successful.", user)
