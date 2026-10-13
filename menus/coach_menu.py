
def coach_menu(user, user_storage):
    if user.role != "Coach" or not user.is_active:
        print("Only an active Coach can enter this panel.")
        return
    print("Welcome, " + user.name + " (" + user.username + ")")
    while True:
        print("--- Coach Panel ---")
        print("1. View Classes")
        print("2. Manage Members' Workout Plans")
        print("3. Logout")

        choice = input("choose an option: ")

        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
