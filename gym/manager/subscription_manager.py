from datetime import timedelta
from gym.models.subscription import SubscriptionPlan, Subscription

class OperationResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data

class SubscriptionManager:
    def __init__(self, repository, member_lookup):
        self.repo = repository
        self.member_lookup = member_lookup

    def create_plan(self, name, price, duration_days):
        try:
            plan = SubscriptionPlan(name, price, duration_days)
            self.repo.add_plan(plan)
            return OperationResult(True, "Plan created successfully.", plan)
        except ValueError as e:
            return OperationResult(False, str(e))

    def get_plan(self, plan_id):
        return self.repo.get_plan_by_id(plan_id)

    def list_plans(self):
        return self.repo.get_all_plans()

    def update_plan(self, plan_id, name, price, duration_days):
        plan = self.repo.get_plan_by_id(plan_id)
        if not plan:
            return OperationResult(False, "Plan not found.")
        
        try:
            temp_plan = SubscriptionPlan(name, price, duration_days, plan_id, plan.is_active)
            self.repo.update_plan(temp_plan)
            return OperationResult(True, "Plan updated successfully.", temp_plan)
        except ValueError as e:
            return OperationResult(False, str(e))

    def deactivate_plan(self, plan_id):
        plan = self.repo.get_plan_by_id(plan_id)
        if not plan:
            return OperationResult(False, "Plan not found.")
        
        plan.is_active = False
        self.repo.update_plan(plan)
        return OperationResult(True, "Plan deactivated successfully.", plan)

    def create_subscription(self, member_username, plan_id, start_date):
        member_username = member_username.strip()
        if not member_username:
            return OperationResult(False, "Username cannot be empty.")
            
        if not self.member_lookup(member_username):
            return OperationResult(False, "Unknown member username.")

        plan = self.repo.get_plan_by_id(plan_id)
        if not plan:
            return OperationResult(False, "Plan not found.")
            
        if not plan.is_active:
            return OperationResult(False, "Cannot subscribe to an inactive plan.")

        end_date = start_date + timedelta(days=plan.duration_days)
        
        try:
            subscription = Subscription(member_username, plan_id, start_date, end_date)
            self.repo.add(subscription)
            return OperationResult(True, "Subscription created successfully.", subscription)
        except ValueError as e:
            return OperationResult(False, str(e))

    def get_subscription(self, subscription_id):
        return self.repo.get_by_id(subscription_id)

    def get_member_subscriptions(self, member_username):
        return self.repo.get_by_member_username(member_username)

    def check_subscription(self, member_username, current_date):
        if not self.member_lookup(member_username):
            return OperationResult(False, "Unknown member username.")
            
        subscriptions = self.repo.get_by_member_username(member_username)
        for sub in subscriptions:
            if sub.is_active(current_date):
                return OperationResult(True, "Active subscription found.", sub)
                
        return OperationResult(False, "No active subscription found for this date.")
    
    def renew_subscription(self, member_username, plan_id, current_date, payment_manager):
        plan = self.repo.get_plan_by_id(plan_id)

        if not plan:
            return OperationResult(False, "Plan not found.")

        if not plan.is_active:
            return OperationResult(False, "This plan is inactive.")

        start_date = current_date
        subscriptions = self.repo.get_by_member_username(member_username)

        for sub in subscriptions:
            if sub.status == "active" and sub.end_date > start_date:
                start_date = sub.end_date

        success, message = payment_manager.pay_from_wallet(
            member_username, plan.price
        )

        if not success:
            return OperationResult(False, message)

        return self.create_subscription(
            member_username, plan_id, start_date
        )
    