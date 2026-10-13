from datetime import timedelta
from gym.models.subscription import SubscriptionPlan, Subscription

class OperationResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data

class SubscriptionManager:
    def __init__(self, repository, is_member_active_lookup):
        self.repo = repository
        self.is_member_active_lookup = is_member_active_lookup

    def create_plan(self, name, price, duration_days):
        try:
            plan = SubscriptionPlan(name, price, duration_days)
            self.repo.add_plan(plan)
            return OperationResult(True, "Plan created successfully.", plan)
        except ValueError as e:
            return OperationResult(False, f"Validation failed: {str(e)}")

    def create_subscription(self, member_username, plan_id, start_date):
        # بررسی وجود و فعال بودن کاربر
        is_active_member = self.is_member_active_lookup(member_username)
        if not is_active_member:
            return OperationResult(False, "Subscription failed: Member does not exist or is inactive.")

        plan = self.repo.get_plan_by_id(plan_id)
        if not plan or not plan.is_active:
            return OperationResult(False, "Subscription failed: Plan not found or inactive.")

        try:
            end_date = start_date + timedelta(days=plan.duration_days)
            sub = Subscription(member_username, plan_id, start_date, end_date)
            self.repo.add_subscription(sub)
            
            # برگرداندن اطلاعات کامل طبق خواسته صورت مسئله
            subscription_info = {
                "member_username": sub.member_username,
                "subscription_type": plan.name,
                "amount": plan.price,
                "start_date": sub.start_date,
                "end_date": sub.end_date,
            }
            return OperationResult(True, "Subscription created successfully.", subscription_info)
        except (ValueError, TypeError) as e:
            return OperationResult(False, f"Validation failed: {str(e)}")

    def get_member_status(self, member_username, current_date):
        subs = self.repo.get_subscriptions_by_username(member_username)
        if not subs:
            return "No Subscription", None

        # پیدا کردن جدیدترین اشتراک کاربر برای بررسی وضعیت
        latest_sub = max(subs, key=lambda s: s.end_date)
        status = latest_sub.get_status(current_date)
        
        plan = self.repo.get_plan_by_id(latest_sub.plan_id)
        info = {
            "subscription_type": plan.name,
            "amount": plan.price,
            "start_date": latest_sub.start_date,
            "end_date": latest_sub.end_date,
            "status": status
        }
        return status, info