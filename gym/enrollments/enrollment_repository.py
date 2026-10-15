
import json
import os

from gym.enrollments.class_enrollment import ClassEnrollment


class EnrollmentRepository:
    def __init__(self, file_path="gym/data/enrollments.json"):
        self.file_path = file_path
        self.enrollments = {}
        if self.load() is False:
            print("Stored enrollment data could not be read.")

    def load(self):
        self.load_failed = False
        self.enrollments = {}

        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                self.load_failed = True
                return False
            loaded_enrollments = {}

            for record in data:
                try:
                    enrollment = ClassEnrollment(
                        enrollment_id=record["enrollment_id"],
                        member_username=record["member_username"],
                        class_name=record["class_name"],
                        registration_date=record["registration_date"],
                        tracking_number=record["tracking_number"],
                        is_active=record["is_active"],
                    )

                    loaded_enrollments[enrollment.enrollment_id] = enrollment

                except (KeyError, TypeError, ValueError):
                    self.load_failed = True
                    continue

            self.enrollments = loaded_enrollments
            return not self.load_failed

        except (OSError, ValueError):
            self.load_failed = True
            return False

    def save(self):
        data = []

        for enrollment in self.enrollments.values():
            data.append({
                "enrollment_id": enrollment.enrollment_id,
                "member_username": enrollment.member_username,
                "class_name": enrollment.class_name,
                "registration_date": enrollment.registration_date,
                "tracking_number": enrollment.tracking_number,
                "is_active": enrollment.is_active,
            })

        try:
            folder = os.path.dirname(os.path.abspath(self.file_path))
            os.makedirs(folder, exist_ok=True)

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file)

            return True

        except (OSError, TypeError, ValueError):
            return False

    def add(self, enrollment):

        if enrollment.enrollment_id in self.enrollments:
            return False

        self.enrollments[enrollment.enrollment_id] = enrollment

        if not self.save():
            del self.enrollments[enrollment.enrollment_id]
            return False

        return True

    def get_by_id(self, enrollment_id):
        return self.enrollments.get(enrollment_id)

    def get_all(self):
        return list(self.enrollments.values())

    def get_by_member_username(self, member_username):
        result = []

        for enrollment in self.enrollments.values():
            if enrollment.member_username == member_username:
                result.append(enrollment)

        return result

    def get_next_enrollment_id(self):
        return max(self.enrollments, default=0) + 1

    def generate_tracking_number(self):
        number = self.get_next_enrollment_id()
        return f"ENR-{number}"

    def get_active_member_usernames(self, class_name):
        members = []
        for enrollment in self.enrollments.values():
            if enrollment.class_name == class_name and enrollment.is_active:
                members.append(enrollment.member_username)
        return members
