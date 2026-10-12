from datetime import timedelta

class SubscriptionPlan:
    def __init__(self, name, price, duration_days, plan_id=None, is_active=True):
        name = name.strip()
        if not name:
            raise ValueError("Plan name cannot be empty or whitespace.")
        if price < 0:
            raise ValueError("Price must be a non-negative numeric value.")
        if duration_days <= 0:
            raise ValueError("Duration must be a positive integer.")
            
        self.plan_id = plan_id
        self.name = name
        self.price = price
        self.duration_days = duration_days
        self.is_active = is_active

class Subscription:
    def __init__(self, member_username, plan_id, start_date, end_date, subscription_id=None, status="active"):
        member_username = member_username.strip()
        if not member_username:
            raise ValueError("Username cannot be empty or whitespace.")
            
        self.subscription_id = subscription_id
        self.member_username = member_username
        self.plan_id = plan_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def is_active(self, current_date):
        if self.status != "active":
            return False
        return self.start_date <= current_date < self.end_date

    def expire(self):
        self.status = "expired"