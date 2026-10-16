
class ClassEnrollment:
    def __init__(
        self,
        enrollment_id,
        member_username,
        class_name,
        registration_date,
        tracking_number,
        is_active=True,
    ):
        if type(enrollment_id) is not int or enrollment_id < 1:
            raise ValueError("Enrollment ID must be a positive integer.")
        self._validate_inputs(member_username, class_name, tracking_number, is_active)

        self.enrollment_id = enrollment_id
        self.member_username = member_username.strip()
        self.class_name = class_name.strip()
        self.registration_date = registration_date
        self.tracking_number = tracking_number.strip()
        self.is_active = is_active

    @staticmethod
    def _validate_inputs(member_username, class_name, tracking_number, is_active):
        if not isinstance(member_username, str) or not member_username.strip():
            raise ValueError("Member username must not be empty.")
        if not isinstance(class_name, str) or not class_name.strip():
            raise ValueError("Class identifier must not be empty.")
        if not isinstance(tracking_number, str) or not tracking_number.strip():
            raise ValueError("Tracking number must not be empty.")
        if not isinstance(is_active, bool):
            raise ValueError("is_active must be a Boolean.")

    @property
    def status(self):
        if self.is_active:
            return "Active"
        return "Cancelled"

    def cancel(self):
        if not self.is_active:
            return False

        self.is_active = False
        return True
