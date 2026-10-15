class GymClass:
    def __init__(
        self,
        name,
        exercise,
        coach_name,
        hall_name,
        day,
        time,
        capacity,
        remaining_capacity=None,
        is_active=True,
    ):
        self._validate_inputs(name, exercise, coach_name,
                              hall_name, day, time, capacity)

        self.name = str(name).strip()
        self.exercise = str(exercise).strip()
        self.coach_name = str(coach_name).strip()
        self.hall_name = str(hall_name).strip()
        self.day = str(day).strip()
        self.time = str(time).strip()
        self.capacity = capacity
        self.remaining_capacity = capacity if remaining_capacity is None else remaining_capacity
        self.is_active = bool(is_active)

    def _validate_inputs(self, name, exercise, coach_name, hall_name, day, time, capacity):
        if not name or not str(name).strip():
            raise ValueError("Class title must not be empty.")
        if not exercise or not str(exercise).strip():
            raise ValueError("Sport type must not be empty.")
        if not coach_name or not str(coach_name).strip():
            raise ValueError("Coach name must not be empty.")
        if not hall_name or not str(hall_name).strip():
            raise ValueError("Hall name must not be empty.")
        if not day or not str(day).strip():
            raise ValueError("Day must not be empty.")
        if not time or not str(time).strip():
            raise ValueError("Time must not be empty.")
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

    def update_details(self, name, exercise, coach_name, hall_name, day, time, capacity):
        self._validate_inputs(name, exercise, coach_name,
                              hall_name, day, time, capacity)

        used_capacity = self.capacity - self.remaining_capacity

        if capacity < used_capacity:
            raise ValueError(
                f"Cannot reduce capacity to {capacity}. There are already {used_capacity} active registrations."
            )

        self.name = str(name).strip()
        self.exercise = str(exercise).strip()
        self.coach_name = str(coach_name).strip()
        self.hall_name = str(hall_name).strip()
        self.day = str(day).strip()
        self.time = str(time).strip()
        self.capacity = capacity
        self.remaining_capacity = capacity - used_capacity

    def assign_coach(self, coach_name):
        if not coach_name or not str(coach_name).strip():
            raise ValueError("Coach name must not be empty.")
        self.coach_name = str(coach_name).strip()

    def assign_hall(self, hall_name):
        if not hall_name or not str(hall_name).strip():
            raise ValueError("Hall name must not be empty.")
        self.hall_name = str(hall_name).strip()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
