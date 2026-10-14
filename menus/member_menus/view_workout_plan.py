def display_workout_plan(authenticated_username, workout_repo):
    print("\n--- Workout Plans ---")
    plans = workout_repo.get_by_member_username(authenticated_username)
    if not plans:
        print("You currently have no workout plan assigned by a coach.")
        return
    for plan in plans:
        print("Class:", plan.class_id, "| Coach:", plan.coach_username)
        if not plan.exercises:
            print("No exercises have been added to this plan yet.")
        for number, exercise in enumerate(plan.exercises, 1):
            print("Exercise", number, ":", exercise.name)
            print("Sets:", exercise.sets, "| Repetitions:", exercise.repetitions)
            print("Rest time:", exercise.rest_time, "seconds")
            print("Description:", exercise.description)
