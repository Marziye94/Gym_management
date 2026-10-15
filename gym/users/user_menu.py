from getpass import getpass


def manage_users_menu(user_manager):
    while True:
        print("--- User Management ---")
        print("1. Add User")
        print("2. Edit User")
        print("3. View Users")
        print("4. Activate or Deactivate User")
        print("5. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            _add_user(user_manager)
        elif choice == "2":
            _edit_user(user_manager)
        elif choice == "3":
            _view_users(user_manager)
        elif choice == "4":
            _change_status(user_manager)
        elif choice == "5":
            return
        else:
            print("Invalid choice. Please try again.")


def display_user(user):
    print("Name:", user.name)
    print("Username:", user.username)
    print("Role:", user.role)
    print("Email:", user.email if user.email is not None else "Not provided")
    print("Account status:", "Active" if user.is_active else "Inactive")
    print()


def _read_role():
    while True:
        print("1. Coach")
        print("2. Member")
        print("3. Back")
        choice = input("Choose the user role: ").strip()
        if choice == "1":
            return "Coach"
        if choice == "2":
            return "Member"
        if choice == "3":
            return None
        print("Invalid choice. Please try again.")


def _read_status(current_status=None):
    while True:
        print("1. Active")
        print("2. Inactive")
        print("3. Back without saving")
        if current_status is not None:
            print("Press Enter to keep the current status.")
        choice = input("Choose account status: ").strip()
        if choice == "1":
            return True
        if choice == "2":
            return False
        if choice == "3":
            return None
        if choice == "" and current_status is not None:
            return current_status
        print("Invalid choice. Please try again.")


def _add_user(user_manager):
    role = _read_role()
    if role is None:
        return

    name = input("Name: ")
    username = input("Username: ")
    password = getpass("Password: ")
    email = input("Email (optional): ")
    is_active = _read_status()
    if is_active is None:
        return

    result = user_manager.add_user(name, username, password, role, email, is_active)
    print(result["message"])


def _edit_user(user_manager):
    username = input("Username to edit (Enter to cancel): ")
    if username == "":
        return
    result = user_manager.find_user(username)
    if not result["success"]:
        print(result["message"])
        return

    user = result["user"]
    display_user(user)
    name = input("New name (Enter to keep): ")
    if name == "":
        name = user.name
    password = getpass("New password (Enter to keep): ")
    email = input("New email (Enter to keep, - to clear): ")
    if email == "":
        email = user.email
    elif email == "-":
        email = None
    is_active = _read_status(user.is_active)
    if is_active is None:
        return

    result = user_manager.edit_user(username, name, password, email, is_active)
    print(result["message"])


def _view_users(user_manager):
    result = user_manager.list_users()
    if not result["success"]:
        print(result["message"])
        return
    if not result["users"]:
        print("No Coach or Member accounts found.")
        return
    for user in result["users"]:
        display_user(user)


def _change_status(user_manager):
    username = input("Username (Enter to cancel): ")
    if username == "":
        return
    result = user_manager.find_user(username)
    if not result["success"]:
        print(result["message"])
        return

    user = result["user"]
    display_user(user)
    is_active = _read_status(user.is_active)
    if is_active is None:
        return
    result = user_manager.set_active(username, is_active)
    print(result["message"])
