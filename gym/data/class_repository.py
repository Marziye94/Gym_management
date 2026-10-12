class ClassRepository:
    def __init__(self):
        self.classes = {}

    def add(self, gym_class):
        if gym_class.name in self.classes:
            return False
        self.classes[gym_class.name] = gym_class
        return True

    def get_class(self, class_name):

        return self.classes.get(class_name, None)

    def get_all(self):
        return list(self.classes.values())

    def update(self, gym_class):
        if gym_class.name not in self.classes:
            return False
        self.classes[gym_class.name] =  gym_class
        return True
