class SubscriptionRepository:
    def __init__(self):
        self.plans = {}
        self.subscriptions = {}
        self.next_plan_id = 1
        self.next_subscription_id = 1

    def add_plan(self, plan):
        if plan.plan_id is not None and plan.plan_id in self.plans:
            raise ValueError("Plan ID already exists.")
            
        if plan.plan_id is None:
            plan.plan_id = self.next_plan_id
            self.next_plan_id += 1
            
        self.plans[plan.plan_id] = plan

    def get_plan_by_id(self, plan_id):
        return self.plans.get(plan_id)

    def get_all_plans(self):
        return list(self.plans.values())

    def update_plan(self, plan):
        if plan.plan_id not in self.plans:
            raise ValueError("Plan does not exist.")
        self.plans[plan.plan_id] = plan

    def add(self, subscription):
        if subscription.subscription_id is not None and subscription.subscription_id in self.subscriptions:
            raise ValueError("Subscription ID already exists.")
            
        if subscription.subscription_id is None:
            subscription.subscription_id = self.next_subscription_id
            self.next_subscription_id += 1
            
        self.subscriptions[subscription.subscription_id] = subscription

    def get_by_id(self, subscription_id):
        return self.subscriptions.get(subscription_id)

    def get_by_member_username(self, member_username):
        user_subs = []
        for sub in self.subscriptions.values():
            if sub.member_username == member_username:
                user_subs.append(sub)
        return user_subs

    def get_all(self):
        return list(self.subscriptions.values())

    def update(self, subscription):
        if subscription.subscription_id not in self.subscriptions:
            raise ValueError("Subscription does not exist.")
        self.subscriptions[subscription.subscription_id] = subscription