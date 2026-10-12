class GymHall:

    def __init__(self, name, capacity, equipment=None):
        self.check(name, capacity)
        self.name = name.strip()
        self.capacity = capacity
        self.equipment = equipment or []
        self.is_active = True

    @staticmethod
    def check(name, capacity):
        if type(name) is not str or name.strip() == "":
            raise ValueError("Hall name must not be empty.")
        if type(capacity) is not int or capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

    def update_details(self, name, capacity, equipment):
        self.check(name, capacity)
        self.name = name.strip()
        self.capacity = capacity
        self.equipment = equipment or []

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def __repr__(self):
        return (f"GymHall(name={self.name!r}, capacity={self.capacity}, "
                f"equipment={self.equipment}, is_active={self.is_active})")
