def show_plan(plan):
    print(f"Plan ID: {plan.plan_id}")
    print(f"Class: {plan.class_id}")
    print(f"Member: {plan.member_username}")
    if not plan.exercises:
        print("No exercises yet.")
        return
    number = 1
    for exercise in plan.exercises:
        print(f"{number}. {exercise.name}")
        print(f"   Sets: {exercise.sets}")
        print(f"   Repetitions: {exercise.repetitions}")
        print(f"   Rest time: {exercise.rest_time} seconds")
        print(f"   Description: {exercise.description}")
        number += 1


def read_integer(prompt, current=None):
    text = input(prompt).strip()
    if text == "" and current is not None:
        return current
    try:
        return int(text)
    except ValueError:
        return text


def read_rest_time(prompt, current=None):
    text = input(prompt).strip()
    if text == "" and current is not None:
        return current
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text


def read_text(prompt, current=None):
    text = input(prompt).strip()
    if text == "" and current is not None:
        return current
    return text


def view_plan_menu(coach, manager, class_name, member_username):
    result = manager.get_plan(coach, class_name, member_username)
    if not result.success:
        print(result.message)
        return
    show_plan(result.data)


def create_plan_menu(coach, manager, class_name, member_username):
    result = manager.create_plan(coach, class_name, member_username)
    print(result.message)


def add_exercise_menu(coach, manager, class_name, member_username):
    name = read_text("Exercise name: ")
    sets = read_integer("Number of sets: ")
    repetitions = read_integer("Number of repetitions: ")
    rest_time = read_rest_time("Rest time in seconds: ")
    description = read_text("Description: ")
    result = manager.add_exercise(coach, class_name, member_username,
                                  name, sets, repetitions, rest_time, description)
    print(result.message)


def edit_exercise_menu(coach, manager, class_name, member_username):
    result = manager.get_plan(coach, class_name, member_username)
    if not result.success:
        print(result.message)
        return
    plan = result.data
    show_plan(plan)
    if not plan.exercises:
        return

    number = read_integer("Exercise number to edit: ")
    exercise = plan.get_exercise(number)
    if exercise is None:
        print("Exercise was not found.")
        return

    print("Press Enter to keep the current value.")
    name = read_text(f"Exercise name ({exercise.name}): ", exercise.name)
    sets = read_integer(f"Number of sets ({exercise.sets}): ", exercise.sets)
    repetitions = read_integer(f"Number of repetitions ({exercise.repetitions}): ", exercise.repetitions)
    rest_time = read_rest_time(f"Rest time in seconds ({exercise.rest_time}): ", exercise.rest_time)
    description = read_text(f"Description ({exercise.description}): ", exercise.description)

    result = manager.update_exercise(coach, class_name, member_username, number,
                                     name, sets, repetitions, rest_time, description)
    print(result.message)


def member_plan_menu(coach, manager, class_name, member_username):
    while True:
        print(f"\n--- Workout Plan: {member_username} ({class_name}) ---")
        print("1. View Plan")
        print("2. Create Plan")
        print("3. Add Exercise")
        print("4. Edit Exercise")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_plan_menu(coach, manager, class_name, member_username)
        elif choice == "2":
            create_plan_menu(coach, manager, class_name, member_username)
        elif choice == "3":
            add_exercise_menu(coach, manager, class_name, member_username)
        elif choice == "4":
            edit_exercise_menu(coach, manager, class_name, member_username)
        elif choice == "5":
            return
        else:
            print("Invalid choice. Please try again.")


def manage_workouts_menu(coach, workout_plan_manager):
    manager = workout_plan_manager
    print("\n--- Manage Member Workout Plans ---")

    classes = manager.get_coach_classes(coach)
    if not classes:
        print("No classes are assigned to you.")
        return
    print("Your classes:")
    for gym_class in classes:
        print(f"- {gym_class.name}")

    class_name = input("Class name (or press Enter to go back): ").strip()
    if class_name == "":
        return
    result = manager.get_coach_class(coach, class_name)
    if not result.success:
        print(result.message)
        return
    class_name = result.data.name

    members = manager.get_active_members(class_name)
    if not members:
        print("This class has no members with an active enrollment.")
        return
    print("Members with an active enrollment:")
    for member in members:
        print(f"- {member}")

    member_username = input("Member username: ").strip()
    result = manager.check_member(coach, class_name, member_username)
    if not result.success:
        print(result.message)
        return

    member_plan_menu(coach, manager, class_name, member_username)