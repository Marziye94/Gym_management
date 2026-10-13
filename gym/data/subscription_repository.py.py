class SubscriptionRepository:
    def __init__(self):
        self._plans = {}
        self._subscriptions = {}
        self._next_plan_id = 1
        self._next_subscription_id = 1

    def add_plan(self, plan):
        if plan.plan_id is None:
            plan.plan_id = self._next_plan_id
            self._next_plan_id += 1
        self._plans[plan.plan_id] = plan

    def get_plan_by_id(self, plan_id):
        return self._plans.get(plan_id)

    def add_subscription(self, subscription):
        if subscription.subscription_id is None:
            subscription.subscription_id = self._next_subscription_id
            self._next_subscription_id += 1
        self._subscriptions[subscription.subscription_id] = subscription

    def get_subscriptions_by_username(self, username):
        # برگرداندن تمام اشتراک‌های یک کاربر بدون پاک کردن تاریخچه
        return [sub for sub in self._subscriptions.values() if sub.member_username == username]