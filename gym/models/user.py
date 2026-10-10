ALLOWED_ROLES = ("Manager", "Coach", "Member")


class User:
    def __init__(
        self,
        user_id,
        username,
        password,
        role,
        is_active=True,
        email=None,
    ):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.is_active = is_active
        self.email = email

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
