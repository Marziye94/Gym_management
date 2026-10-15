
import os
import sys
from datetime import date, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from gym.users.user import User
from gym.classes.gym_class import GymClass
from gym.subscriptions.subscription import SubscriptionPlan, Subscription
from gym.enrollments.class_enrollment import ClassEnrollment

from gym.users.user_repository import UserStorage
from gym.classes.class_repository import ClassRepository
from gym.subscriptions.subscription_repository import SubscriptionRepository
from gym.enrollments.enrollment_repository import EnrollmentRepository

from gym.subscriptions.subscription_service import SubscriptionManager
from gym.enrollments.enrollment_service import ClassEnrollmentManager


DEMO_DATA = os.path.join(PROJECT_ROOT, "demos", "data")

USERS_FILE = os.path.join(DEMO_DATA, "users_enrollment_demo.json")
CLASSES_FILE = os.path.join(DEMO_DATA, "classes_enrollment_demo.json")
SUBSCRIPTIONS_FILE = os.path.join(
    DEMO_DATA, "subscriptions_enrollment_demo.json"
)
ENROLLMENTS_FILE = os.path.join(
    DEMO_DATA, "enrollments_demo.json"
)


def is_active_member(username, user_storage):
    users = user_storage.load_users()
    user = user_storage.find_by_username(users, username)

    return (
        user is not None
        and user.role == "Member"
        and user.is_active
    )


def show_classes(class_repository, enrollment_manager):
    print("\n--- Available Classes ---")

    for gym_class in class_repository.get_all():
        remaining = enrollment_manager.get_remaining_capacity(
            gym_class.name
        )

        print(f"\nTitle: {gym_class.name}")
        print(f"Sport type: {gym_class.exercise}")
        print(f"Coach: {gym_class.coach_name}")
        print(f"Hall: {gym_class.hall_name}")
        print(f"Day: {gym_class.day}")
        print(f"Time: {gym_class.time}")
        print(f"Total capacity: {gym_class.capacity}")
        print(f"Remaining capacity: {remaining}")

        if not gym_class.is_active:
            print("Status: Unavailable (inactive)")
        elif remaining <= 0:
            print("Status: Unavailable (full)")
        else:
            print("Status: Available")


def show_registrations(enrollment_manager, username):
    print(f"\n--- Registrations for {username} ---")

    enrollments = enrollment_manager.get_member_enrollments(username)

    if not enrollments:
        print("No registrations found.")
        return

    for enrollment in enrollments:
        print(f"Class: {enrollment.class_name}")
        print(f"Registration date: {enrollment.registration_date}")
        print(f"Status: {enrollment.status}")
        print(f"Tracking number: {enrollment.tracking_number}")
        print(f"Registration ID: {enrollment.enrollment_id}")
        print()


def run_demo():
    os.makedirs(DEMO_DATA, exist_ok=True)

    # 1. Create demo users.
    user_storage = UserStorage(USERS_FILE)

    users = [
        User(
            1, "Reza Ahmadi", "reza123",
            "Reza123@", "Member", True, "reza@test.com"
        ),
        User(
            2, "Sara Kamali", "sara123",
            "Sara123@", "Member", True, "sara@test.com"
        ),
    ]

    user_storage.save_users(users)

    # 2. Create demo classes.
    class_repository = ClassRepository(CLASSES_FILE)

    yoga = GymClass(
        name="Yoga",
        exercise="Yoga",
        coach_name="Reza Coach",
        hall_name="Main Hall",
        day="Saturday",
        time="10:00",
        capacity=2,
        is_active=True,
    )

    inactive_class = GymClass(
        name="Inactive Fitness",
        exercise="Fitness",
        coach_name="Sara Coach",
        hall_name="Studio Hall",
        day="Sunday",
        time="12:00",
        capacity=5,
        is_active=False,
    )

    class_repository.add(yoga)
    class_repository.add(inactive_class)

    # 3. Create an active subscription for Reza.
    subscription_repository = SubscriptionRepository(
        SUBSCRIPTIONS_FILE
    )

    today = date.today()

    plan = SubscriptionPlan("Demo Plan", 1000, 30)
    subscription_repository.add_plan(plan)

    subscription = Subscription(
        member_username="reza123",
        plan_id=plan.plan_id,
        start_date=today - timedelta(days=1),
        end_date=today + timedelta(days=29),
    )

    subscription_repository.add_subscription(subscription)

    subscription_manager = SubscriptionManager(
        subscription_repository,
        lambda username: is_active_member(username, user_storage),
    )

    # 4. Create enrollment repository and manager.
    enrollment_repository = EnrollmentRepository(ENROLLMENTS_FILE)

    enrollment_manager = ClassEnrollmentManager(
        enrollment_repository,
        class_repository,
        user_storage,
        subscription_manager,
    )

    # Reset enrollment data so the demo has the same initial state.
    enrollment_repository.enrollments = {}

    existing_enrollment = ClassEnrollment(
        enrollment_id=1,
        member_username="another_member",
        class_name="Yoga",
        registration_date=today.isoformat(),
        tracking_number="ENR-1",
        is_active=True,
    )

    enrollment_repository.add(existing_enrollment)

    # 5. View classes and remaining capacity.
    print("\nSTEP 1: View classes")
    show_classes(class_repository, enrollment_manager)

    # 6. Register Reza successfully.
    print("\nSTEP 2: Register Reza for Yoga")
    success, message = enrollment_manager.register_member(
        "reza123", "Yoga"
    )
    print(message)

    # 7. Try registering Reza for Yoga again.
    print("\nSTEP 3: Try duplicate registration")
    success, message = enrollment_manager.register_member(
        "reza123", "Yoga"
    )
    print(message)

    # 8. Sara has no active subscription.
    print("\nSTEP 4: Register Sara for Yoga")
    success, message = enrollment_manager.register_member(
        "sara123", "Yoga"
    )
    print(message)

    # 9. Try registering for an inactive class.
    print("\nSTEP 5: Register Reza for an inactive class")
    success, message = enrollment_manager.register_member(
        "reza123", "Inactive Fitness"
    )
    print(message)

    # 10. View Reza's registrations.
    print("\nSTEP 6: View Reza's registrations")
    show_registrations(enrollment_manager, "reza123")

    # 11. Cancel Reza's Yoga registration.
    print("\nSTEP 7: Cancel Reza's Yoga registration")

    reza_enrollments = enrollment_manager.get_member_enrollments(
        "reza123"
    )

    for enrollment in reza_enrollments:
        if enrollment.class_name == "Yoga" and enrollment.is_active:
            success, message = enrollment_manager.cancel_enrollment(
                "reza123", enrollment.enrollment_id
            )
            print(message)
            break

    # 12. Show capacity after cancellation.
    print("\nSTEP 8: Check capacity after cancellation")
    print(
        "Remaining capacity:",
        enrollment_manager.get_remaining_capacity("Yoga"),
    )

    # 13. Reload the repository and verify persistence.
    print("\nSTEP 9: Reload enrollment data")

    reloaded_repository = EnrollmentRepository(ENROLLMENTS_FILE)

    for enrollment in reloaded_repository.get_by_member_username(
        "reza123"
    ):
        print(f"Class: {enrollment.class_name}")
        print(f"Status: {enrollment.status}")
        print(f"Tracking number: {enrollment.tracking_number}")


if __name__ == "__main__":
    run_demo()
