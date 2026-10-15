import math
from datetime import date

class SubscriptionPlan:
    def __init__(self, name, price, duration_days, plan_id=None, is_active=True):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Plan name must be a non-empty string.")
        if type(price) not in (int, float) or not math.isfinite(price) or price <= 0:
            raise ValueError("Price must be a numeric value greater than zero.")
        if type(duration_days) is not int or duration_days <= 0:
            raise ValueError("Duration must be a positive integer.")
            
        self.plan_id = plan_id
        self.name = name.strip()
        self.price = float(price)
        self.duration_days = duration_days
        self.is_active = is_active

class Subscription:
    def __init__(self, member_username, plan_id, start_date, end_date, subscription_id=None, payment_id=None):
        if not isinstance(member_username, str) or not member_username.strip():
            raise ValueError("Member username must be a non-empty string.")
        if not isinstance(start_date, date) or not isinstance(end_date, date):
            raise ValueError("Start date and end date must be valid date objects.")
        if end_date <= start_date:
            raise ValueError("End date must be later than start date.")
            
        self.subscription_id = subscription_id
        self.payment_id = payment_id
        self.member_username = member_username.strip()
        self.plan_id = plan_id
        self.start_date = start_date
        self.end_date = end_date

    def get_status(self, current_date):
        if self.start_date <= current_date < self.end_date:
            return "Active"
        return "Expired"