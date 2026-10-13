from gym.manager.class_manager import ClassManager
from gym.data.class_repository import ClassRepository
import sys
sys.path.append(".")


def show_class(gym_class):
    if gym_class.is_active:
        status = "Active"
    else:
        status = "Inactive"

    print(f"Title: {gym_class.name}")
    print(f"Sport Type: {gym_class.exercise}")
    print(f"Coach: {gym_class.coach_name}")
    print(f"Hall: {gym_class.hall_name}")
    print(f"Day: {gym_class.day}")
    print(f"Time: {gym_class.time}")
    print(f"Capacity: {gym_class.capacity}")
    print(f"Status: {status}")


coaches = {
    "Sara": True,
    "Reza": True,
    "Inactive Coach": False,
}

halls = {
    "Main Hall": True,
    "Studio Hall": True,
    "Inactive Hall": False,
}


def check_coach(name):
    if name in coaches and coaches[name] == True:
        return True
    return False


def check_hall(name):
    if name in halls and halls[name] == True:
        return True
    return False


repo = ClassRepository()
manager = ClassManager(repo, check_coach, check_hall)

# Step 1: Create a Class
res1 = manager.create_class(
    name="Morning Yoga",
    exercise="Yoga",
    coach_name="Sara",
    hall_name="Main Hall",
    day="Saturday",
    time="10:00",
    capacity=15
)
print("--- Created Class ---\n")
show_class(res1.data)
print()


res2 = manager.update_class(
    original_name="Morning Yoga",
    new_name="Evening Fitness",
    exercise="Fitness",
    coach_name="Reza",
    hall_name="Studio Hall",
    day="Sunday",
    time="18:00",
    capacity=20
)
print("--- Updated Class ---\n")
show_class(res2.data)
print()


res3 = manager.update_class(
    original_name="Evening Fitness",
    new_name="Invalid Class",
    exercise="Fitness",
    coach_name="Inactive Coach",
    hall_name="Studio Hall",
    day="Monday",
    time="19:00",
    capacity=25
)
print(res3.message)
print()

current_class = manager.get_class("Evening Fitness").data
show_class(current_class)
print()


deact_res = manager.deactivate_class("Evening Fitness")
if deact_res.data.is_active:
    print("Status: Active\n")
else:
    print("Status: Inactive\n")

act_res = manager.activate_class("Evening Fitness")
if act_res.data.is_active:
    print("Status: Active")
else:
    print("Status: Inactive")
