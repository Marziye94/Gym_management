def format_status(hall):
    if hall.is_active:
        return "Active"
    return "Inactive"


def show_hall(hall):
    print(f"Name: {hall.name}")
    print(f"Capacity: {hall.capacity}")
    print(f"Equipment: {', '.join(hall.equipment)}")
    print(f"Status: {format_status(hall)}")


def read_capacity(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Capacity must be a positive integer.")
        return None


def read_equipment(prompt):
    equipment_input = input(prompt)
    return [item.strip() for item in equipment_input.split(",") if item.strip()]


def add_hall_menu(hall_manager):
    name = input("Hall name: ")
    capacity = read_capacity("Capacity: ")
    if capacity is None:
        return
    equipment = read_equipment("Equipment, separated by commas: ")

    print("Status:")
    print("1. Active")
    print("2. Inactive")
    status = input("Choose status: ").strip()
    if status == "1":
        is_active = True
    elif status == "2":
        is_active = False
    else:
        print("Invalid status. The hall was not created.")
        return

    result = hall_manager.create_hall(name, capacity, equipment, is_active)
    print(result.message)


def edit_hall_menu(hall_manager):
    current_name = input("Current hall name: ").strip()
    hall = hall_manager.get_hall(current_name)
    if hall is None:
        print(f"Hall '{current_name}' was not found.")
        return

    print(f"Current name: {hall.name}")
    print(f"Current capacity: {hall.capacity}")
    print(f"Current equipment: {', '.join(hall.equipment)}")
    print(f"Current status: {format_status(hall)}")

    new_name = input("New hall name: ")
    new_capacity = read_capacity("New capacity: ")
    if new_capacity is None:
        return
    new_equipment = read_equipment("New equipment, separated by commas: ")

    result = hall_manager.update_hall(current_name, new_name, new_capacity, new_equipment)
    print(result.message)


def view_halls_menu(hall_manager):
    halls = hall_manager.list_halls()
    if not halls:
        print("No halls have been registered.")
        return
    for hall in halls:
        show_hall(hall)
        print("-" * 30)


def change_hall_status_menu(hall_manager):
    name = input("Hall name: ").strip()
    hall = hall_manager.get_hall(name)
    if hall is None:
        print(f"Hall '{name}' was not found.")
        return

    print(f"Current status: {format_status(hall)}")
    print("1. Activate")
    print("2. Deactivate")
    print("3. Back")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        result = hall_manager.activate_hall(name)
        print(result.message)
    elif choice == "2":
        result = hall_manager.deactivate_hall(name)
        print(result.message)
    elif choice == "3":
        return
    else:
        print("Invalid choice.")


def manage_halls_menu(hall_manager):
    while True:
        print("\n--- Hall Management ---")
        print("1. Add Hall")
        print("2. Edit Hall")
        print("3. View Halls")
        print("4. Activate or Deactivate Hall")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_hall_menu(hall_manager)
        elif choice == "2":
            edit_hall_menu(hall_manager)
        elif choice == "3":
            view_halls_menu(hall_manager)
        elif choice == "4":
            change_hall_status_menu(hall_manager)
        elif choice == "5":
            return
        else:
            print("Invalid choice. Please try again.")