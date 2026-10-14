def show_class(gym_class, members):
    print(f"Title: {gym_class.name}")
    print(f"Sport type: {gym_class.exercise}")
    print(f"Day: {gym_class.day}")
    print(f"Time: {gym_class.time}")
    print(f"Hall: {gym_class.hall_name}")
    print(f"Capacity: {gym_class.capacity}")
    if members:
        print(f"Registered Members: {', '.join(members)}")
    else:
        print("Registered Members: None")


def view_my_classes_menu(coach, workout_plan_manager):
    print("\n--- My Classes ---")
    classes = workout_plan_manager.get_coach_classes(coach)
    if not classes:
        print("No classes are assigned to you.")
        return
    for gym_class in classes:
        members = workout_plan_manager.get_active_members(gym_class.name)
        show_class(gym_class, members)
        print("-" * 30)