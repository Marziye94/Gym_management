
def manage_classes_menu(member_username, class_repository, enrollment_manager):
    while True:
        print("1. View Available Classes")
        print("2. Register for a Class")
        print("3. View My Registrations")
        print("4. Cancel Registration")
        print("5. Back")

        choice = input("choose an option: ")

        if choice == "1":
            classes = class_repository.get_all()

            if not classes:
                print("No classes found.")
                continue

            for gym_class in classes:
                remaining = enrollment_manager.get_remaining_capacity(gym_class.name)

                print(f"\nTitle: {gym_class.name}")
                print(f"Sport type: {gym_class.exercise}")
                print(f"Coach: {gym_class.coach_name}")
                print(f"Hall: {gym_class.hall_name}")
                print(f"Day: {gym_class.day}")
                print(f"Time: {gym_class.time}")
                print(f"Total capacity: {gym_class.capacity}")
                print(f"Remaining capacity: {remaining}")

                if not gym_class.is_active:
                    print("Status: Unavailable (inactive)")
                elif remaining <= 0:
                    print("Status: Unavailable (full)")
                else:
                    print("Status: Available")

        elif choice == "2":
            class_name = input("Enter class title: ").strip()

            success, message = enrollment_manager.register_member(member_username, class_name)

            print(message)

        elif choice == "3":
            enrollments = enrollment_manager.get_member_enrollments(member_username)

            if not enrollments:
                print("You have no class registrations.")
                continue

            for enrollment in enrollments:
                print(f"\nClass: {enrollment.class_name}")
                print(f"Registration date: {enrollment.registration_date}")
                print(f"Status: {enrollment.status}")
                print(f"Tracking number: {enrollment.tracking_number}")

        elif choice == "4":
            enrollments = enrollment_manager.get_member_enrollments(member_username)

            active_enrollments = []

            for enrollment in enrollments:
                if enrollment.is_active:
                    active_enrollments.append(enrollment)

            if not active_enrollments:
                print("You have no active registrations to cancel.")
                continue

            for enrollment in active_enrollments:
                print(f"ID: {enrollment.enrollment_id}")
                print(f"Class: {enrollment.class_name}")

            enrollment_id = input("Enter registration ID to cancel: ").strip()

            if not enrollment_id.isdigit():
                print("Invalid registration ID.")
                continue

            success, message = enrollment_manager.cancel_enrollment(
                member_username,
                int(enrollment_id)
                )

            print(message)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")
