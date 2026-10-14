from gym.data.errors import StorageError
from gym.classes.coach_class_menu import view_my_classes_menu
from gym.workouts.coach_workout_menu import manage_workouts_menu


def coach_menu(user, application):
    if user.role != "Coach" or not user.is_active:
        print("Only an active Coach can enter this panel.")
        return
    print("Welcome, " + user.name + " (" + user.username + ")")
    while True:
        print("--- Coach Panel ---")
        print("1. View My Classes")
        print("2. Manage Member Workout Plans")
        print("3. Logout")
        choice = input("Choose an option: ").strip()
        if choice == "3":
            return
        if choice not in ("1", "2"):
            print("Invalid choice. Please try again.")
            continue
        if application["workout_manager"] is None:
            print("Coach class and workout features are unavailable.")
            continue
        try:
            if choice == "1":
                view_my_classes_menu(user, application["workout_manager"])
            elif choice == "2":
                manage_workouts_menu(user, application["workout_manager"])
        except (OSError, ValueError, StorageError) as error:
            print("Could not open or complete this feature:", error)
