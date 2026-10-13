import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from gym.manager.class_manager import ClassManager
from gym.data.class_repository import ClassRepository


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


demo_file = os.path.join(PROJECT_ROOT, "demos", "data", "classes_fix_demo.json")
os.makedirs(os.path.dirname(demo_file), exist_ok=True)
with open(demo_file, "w", encoding="utf-8") as file:
    file.write("[]")
repo = ClassRepository(data_file=demo_file)
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
    current_name="Morning Yoga",
    new_name="Evening Fitness",
    new_exercise="Fitness",
    new_coach_name="Reza",
    new_hall_name="Studio Hall",
    new_day="Sunday",
    new_time="18:00",
    new_capacity=20
)
print("--- Updated Class ---\n")
show_class(res2.data)
print()


res3 = manager.update_class(
    current_name="Evening Fitness",
    new_name="Invalid Class",
    new_exercise="Fitness",
    new_coach_name="Inactive Coach",
    new_hall_name="Studio Hall",
    new_day="Monday",
    new_time="19:00",
    new_capacity=25
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
