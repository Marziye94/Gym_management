def display_workout_plan(authenticated_username, workout_repo):
    print("\n" + "="*30)
    print("         WORKOUT PLAN")
    print("="*30)
    
    try:
        plan = workout_repo.get_plan_by_username(authenticated_username)
        
        if not plan or not getattr(plan, 'exercises', []):
            print("You currently have no workout plan assigned by a coach.")
            print("==============================\n")
            return
            
        for index, exercise in enumerate(plan.exercises, 1):
            print(f"\nExercise {index}: {getattr(exercise, 'name', 'Unknown')}")
            print(f"  Sets: {getattr(exercise, 'sets', '-')} | Reps: {getattr(exercise, 'reps', '-')}")
            print(f"  Rest Time: {getattr(exercise, 'rest_time', '-')} seconds")
            print(f"  Description: {getattr(exercise, 'description', 'None')}")
            
    except Exception:
        print("Notice: Workout plan data is currently unavailable.")
    
    print("\n==============================\n")
