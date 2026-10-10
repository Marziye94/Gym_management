import re


USERNAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]{2,29}$")
PASSWORD_LETTER_PATTERN = re.compile(r"[A-Za-z]")
PASSWORD_DIGIT_PATTERN = re.compile(r"[0-9]")
PASSWORD_SPECIAL_PATTERN = re.compile(r"[@&]")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+$")


def validation_result(is_valid, message):
    return {"is_valid": is_valid, "message": message}


def validate_username(username):
    if not isinstance(username, str):
        return validation_result(False, "Username must be a string.")

    if username == "":
        return validation_result(False, "Username cannot be empty.")

    if USERNAME_PATTERN.fullmatch(username) is None:
        message = (
            "Username must be 3-30 characters, start with an English letter, "
            "and contain only English letters, digits, or underscores."
        )
        return validation_result(False, message)

    return validation_result(True, "Username is valid.")


def validate_password(password):
    if not isinstance(password, str):
        return validation_result(False, "Password must be a string.")

    if password == "":
        return validation_result(False, "Password cannot be empty.")

    if PASSWORD_LETTER_PATTERN.search(password) is None:
        return validation_result(False, "Password must contain an English letter.")

    if PASSWORD_DIGIT_PATTERN.search(password) is None:
        return validation_result(False, "Password must contain a digit.")

    if PASSWORD_SPECIAL_PATTERN.search(password) is None:
        return validation_result(False, "Password must contain @ or &.")

    return validation_result(True, "Password is valid.")


def validate_email(email):
    if email is None or email == "":
        return validation_result(True, "Email is optional.")

    if not isinstance(email, str):
        return validation_result(False, "Email must be a string.")

    if EMAIL_PATTERN.fullmatch(email) is None:
        message = "Email must contain @ and a dot in the domain part."
        return validation_result(False, message)

    return validation_result(True, "Email is valid.")
