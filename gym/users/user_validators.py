import re


def validation_result(is_valid, message):
    return {"is_valid": is_valid, "message": message}


def validate_name(name):
    if not isinstance(name, str) or not name.strip():
        return validation_result(False, "Name must be a non-empty string.")
    return validation_result(True, "Name is valid.")


def validate_username(username):
    if not isinstance(username, str):
        return validation_result(False, "Username must be a string.")

    username = username.strip()
    if not username:
        return validation_result(False, "Username cannot be empty or whitespace-only.")

    if re.fullmatch(r"[A-Za-z0-9_]+", username) is None:
        return validation_result(False, "Username may contain only English letters, digits, and underscores.")

    return validation_result(True, "Username is valid.")


def validate_password(password):
    if not isinstance(password, str):
        return validation_result(False, "Password must be a string.")

    if password == "":
        return validation_result(False, "Password cannot be empty.")

    if re.search(r"[A-Za-z]", password) is None:
        return validation_result(False, "Password must contain an English letter.")

    if re.search(r"[0-9]", password) is None:
        return validation_result(False, "Password must contain a digit.")

    if re.search(r"[@&]", password) is None:
        return validation_result(False, "Password must contain @ or &.")

    return validation_result(True, "Password is valid.")


def validate_email(email):
    if email is None or email == "":
        return validation_result(True, "Email is optional.")

    if not isinstance(email, str):
        return validation_result(False, "Email must be a string.")

    if re.search(r"@[^@]*\.", email) is None:
        message = "Email must contain @ and a dot in the domain part."
        return validation_result(False, message)

    return validation_result(True, "Email is valid.")
