class HallRepository:
    def __init__(self):
        self.halls = {}

    def add(self, hall):
        if hall.name in self.halls:
            return f"Hall '{hall.name}' already exists."
        self.halls[hall.name] = hall
        return f"Hall '{hall.name}' was added."

    def get_by_name(self, hall_name):
        if hall_name in self.halls:
            return self.halls[hall_name]
        return f"Hall '{hall_name}' was not found."

    def get_all(self):
        return list(self.halls.values())

    def update(self, hall):
        if hall.name not in self.halls:
            return f"Hall '{hall.name}' was not found."
        self.halls[hall.name] = hall
        return f"Hall '{hall.name}' was updated."
