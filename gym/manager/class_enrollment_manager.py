from datetime import date
from gym.models.class_enrollment import ClassEnrollment


class ClassEnrollmentManager:
    def __init__(
        self,
        enrollment_repository,
        class_repository,
        user_storage,
        subscription_manager,
    ):
        self.enrollment_repository = enrollment_repository
        self.class_repository = class_repository
        self.user_storage = user_storage
        self.subscription_manager = subscription_manager

    def get_remaining_capacity(self, class_name):
        gym_class = self.class_repository.get_class(class_name)

        if gym_class is None:
            return None

        active_count = 0

        for enrollment in self.enrollment_repository.get_all():
            if enrollment.class_name == class_name and enrollment.is_active:
                active_count += 1

        return gym_class.capacity - active_count

    def register_member(self, member_username, class_name):
        users = self.user_storage.load_users()
        member = self.user_storage.find_by_username(users, member_username)

        if member is None or member.role != "Member" or not member.is_active:
            return False, "Member does not exist or is inactive."

        today = date.today()

        result = self.subscription_manager.check_subscription(member_username, today)

        if not result.success:
            return False, result.message

        gym_class = self.class_repository.get_class(class_name)

        if gym_class is None:
            return False, "Class not found."

        if not gym_class.is_active:
            return False, "This class is inactive."

        for enrollment in self.enrollment_repository.get_all():
            if (
                enrollment.member_username == member_username
                and enrollment.class_name == class_name
                and enrollment.is_active
            ):
                return False, "You are already registered for this class."

        if self.get_remaining_capacity(class_name) <= 0:
            return False, "This class is full."

        enrollment = ClassEnrollment(
            enrollment_id=self.enrollment_repository.get_next_enrollment_id(),
            member_username=member_username,
            class_name=class_name,
            registration_date=today.isoformat(),
            tracking_number=self.enrollment_repository.generate_tracking_number(),
        )

        if not self.enrollment_repository.add(enrollment):
            return False, "Registration could not be saved."

        return True, "Registration successful."

    def get_member_enrollments(self, member_username):
        return self.enrollment_repository.get_by_member_username(member_username)

    def cancel_enrollment(self, member_username, enrollment_id):
        enrollment = self.enrollment_repository.get_by_id(enrollment_id)

        if enrollment is None:
            return False, "Registration not found."

        if enrollment.member_username != member_username:
            return False, "This registration does not belong to you."

        if not enrollment.is_active:
            return False, "This registration is already cancelled."

        enrollment.cancel()

        if not self.enrollment_repository.save():
            enrollment.is_active = True
            return False, "Cancellation could not be saved."

        return True, "Registration cancelled successfully."