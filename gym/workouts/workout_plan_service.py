import copy

class WorkoutPlanManager:
    def __init__(self, repository):
        self.repository = repository

    def create_plan(self, member_username, exercises):
        try:
            from gym.workouts.workout_plan import WorkoutPlan
            plan = WorkoutPlan(member_username, exercises)
            success, message = self.repository.add(plan)
            if not success:
                return False, message
            return True, "Workout plan created successfully."
        except Exception as error:
            return False, str(error)

    def add_exercise(self, member_username, exercise):
        plan = self.repository.get_plan_by_username(member_username)
        if not plan:
            return False, "Workout plan not found."
            
        previous_exercises = copy.deepcopy(plan.exercises)
        
        plan.exercises.append(exercise)
        
        success, message = self.repository.update(plan)
        if not success:
            plan.exercises = previous_exercises
            return False, message
            
        return True, "Exercise added successfully."
