class GymClass:
    def __init__(self, name, exercise, coach_name, hall_name, schedule, capacity):
        self._validate_inputs(name, schedule, capacity)

        self.name = str(name).strip()
        self.exercise = str(exercise).strip() if exercise else ""
        self.coach_name = str(coach_name).strip() if coach_name else ""
        self.hall_name = str(hall_name).strip() if hall_name else ""
        self.schedule = str(schedule).strip()
        self.capacity = capacity
        self.is_active = True

    def _validate_inputs(self, name, schedule, capacity):
        """اعتبارسنجی مقادیر ورودی بر  اساس دستورات تیم‌لید"""
        if not name or not str(name).strip():
            raise ValueError("نام کلاس نمی‌تواند خالی یا فقط شامل فاصله باشد.")
        if not schedule or not str(schedule).strip():
            raise ValueError("برنامه زمانی (روز و ساعت) نمی‌تواند خالی باشد.")
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError(
                "ظرفیت کلاس باید یک عدد صحیح و بزرگتر از صفر باشد.")

    def update_details(self, name, exercise, schedule, capacity):
        self._validate_inputs(name, schedule, capacity)
        self.name = str(name).strip()
        self.exercise = str(exercise).strip() if exercise else ""
        self.schedule = str(schedule).strip()
        self.capacity = capacity

    def assign_coach(self, coach_name):
        if not coach_name or not str(coach_name).strip():
            raise ValueError("نام مربی نمی‌تواند خالی باشد.")
        self.coach_name = str(coach_name).strip()

    def assign_hall(self, hall_name):
        if not hall_name or not str(hall_name).strip():
            raise ValueError("نام سالن نمی‌تواند خالی باشد.")
        self.hall_name = str(hall_name).strip()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
