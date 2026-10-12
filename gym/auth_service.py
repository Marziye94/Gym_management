from gym.data.errors import StorageError
from gym.data.user_storage import UserStorage
from gym.models.user import ALLOWED_ROLES, User
from gym.validators import validate_email, validate_password, validate_username


def auth_result(success, message, user=None):
    return {
        "success": success,
        "message": message,
        "user": user,
    }


class AuthService:
    def __init__(self):
        self.user_storage = UserStorage()

    def register_user(self, username, password, role, email=None):
        username_result = validate_username(username)
        if not username_result["is_valid"]:
            return auth_result(False, username_result["message"])

        password_result = validate_password(password)
        if not password_result["is_valid"]:
            return auth_result(False, password_result["message"])

        email_result = validate_email(email)
        if not email_result["is_valid"]:
            return auth_result(False, email_result["message"])

        if role not in ALLOWED_ROLES:
            message = "Role must be Manager, Coach, or Member."
            return auth_result(False, message)

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
        user = User(user_id, username, password, role, True, email)
        users.append(user)

        try:
            self.user_storage.save_users(users)
        except StorageError as error:
            return auth_result(False, "Registration failed: " + str(error))

        return auth_result(True, "Registration successful.", user)

    def login(self, username, password):
        if not isinstance(username, str) or not isinstance(password, str):
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
