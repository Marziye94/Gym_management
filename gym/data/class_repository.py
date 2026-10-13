class ClassRepository:
    def __init__(self):
        self.classes = {}

    def add(self, gym_class):
        if gym_class.name in self.classes:
            return False
        self.classes[gym_class.name] = gym_class
        return True

    def get_class(self, class_name):
        if not class_name or not isinstance(class_name, str):
            return None
        return self.classes.get(class_name.strip(), None)

    def get_all(self):
        return list(self.classes.values())

    def update(self, gym_class, old_name=None):
        target_name = old_name.strip() if old_name else gym_class.name
        if target_name not in self.classes:
            return False

        if target_name != gym_class.name:
            del self.classes[target_name]

        self.classes[gym_class.name] = gym_class
        return True