def create_class_menu(class_manager):
    title = input("Class title: ").strip()
    sport_type = input("Sport type: ").strip()
    coach = input("Coach: ").strip()
    hall = input("Hall: ").strip()
    day = input("Day: ").strip()
    time = input("Time: ").strip()
    cap_str = input("Capacity: ").strip()

    try:
        capacity = int(cap_str)
    except ValueError:
        capacity = cap_str

    result = class_manager.create_class(
        title, sport_type, coach, hall, day, time, capacity)
    print(result.message)


def edit_class_menu(class_manager):
    current_title = input("Current class title: ").strip()
    res = class_manager.get_class(current_title)

    if not res.success:
        print(res.message)
        return

    gym_class = res.data

    if gym_class.is_active:
        status = "Active"
    else:
        status = "Inactive"


    print(f"Current title: {gym_class.name}")
    print(f"Current sport type: {gym_class.exercise}")
    print(f"Current coach: {gym_class.coach_name}")
    print(f"Current hall: {gym_class.hall_name}")
    print(f"Current day: {gym_class.day}")
    print(f"Current time: {gym_class.time}")
    print(f"Current capacity: {gym_class.capacity}")
    print(f"Current status: {status}")

    new_title = input("New title: ").strip()
    new_sport = input("New sport type: ").strip()
    new_coach = input("New coach: ").strip()
    new_hall = input("New hall: ").strip()
    new_day = input("New day: ").strip()
    new_time = input("New time: ").strip()
    new_cap_str = input("New capacity: ").strip()

    try:
        new_capacity = int(new_cap_str)
    except ValueError:
        new_capacity = new_cap_str

    update_res = class_manager.update_class(
        gym_class.name, new_title, new_sport, new_coach, new_hall, new_day, new_time, new_capacity
    )
    print(update_res.message)


def change_class_status_menu(class_manager):
    title = input("Class title: ").strip()
    res = class_manager.get_class(title)

    if not res.success:
        print(res.message)
        return

    gym_class = res.data

    if gym_class.is_active:
        status = "Active"
    else:
        status = "Inactive"


    print(f"Current status: {status}\n")
    print("1. Activate")
    print("2. Deactivate")
    print("3. Back")

    op = input("Selected operation: ").strip()
    if op == "1":
        act_res = class_manager.activate_class(gym_class.name)
        print(act_res.message)
    elif op == "2":
        deact_res = class_manager.deactivate_class(gym_class.name)
        print(deact_res.message)
    elif op == "3":
        return
    else:
        print("Invalid choice.")


def view_classes_menu(class_manager, enrollment_manager=None):
    res = class_manager.list_classes()
    classes = res.data

    if len(classes) == 0:
        print("No classes have been registered.")
        return

    for gym_class in classes:
        if enrollment_manager is None:
            remaining = class_manager.get_remaining_capacity(gym_class.name)
        else:
            remaining = enrollment_manager.get_remaining_capacity(gym_class.name)
        if gym_class.is_active:
            status = "Active"
        else:
            status = "Inactive"

        print(f"Title: {gym_class.name}")
        print(f"Sport Type: {gym_class.exercise}")
        print(f"Coach: {gym_class.coach_name}")
        print(f"Hall: {gym_class.hall_name}")
        print(f"Day: {gym_class.day}")
        print(f"Time: {gym_class.time}")
        print(f"Total Capacity: {gym_class.capacity}")
        print(f"Remaining Capacity: {remaining}")
        print(f"Status: {status}")
        print("-" * 30)


def manage_classes_menu(class_manager, enrollment_manager=None):
    while True:
        print("--- Class Management ---")
        print("1. Create Class")
        print("2. Edit Class")
        print("3. Activate or Deactivate Class")
        print("4. View Classes")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_class_menu(class_manager)
        elif choice == "2":
            edit_class_menu(class_manager)
        elif choice == "3":
            change_class_status_menu(class_manager)
        elif choice == "4":
            view_classes_menu(class_manager, enrollment_manager)
        elif choice == "5":
            return
        else:
            print("Invalid choice. Please try again.")
