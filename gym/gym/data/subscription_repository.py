import json
import os
from datetime import date
from gym.models.subscription import SubscriptionPlan, Subscription

class SubscriptionRepository:
    def __init__(self, file_path="gym/data/subscriptions.json"):
        self.file_path = file_path
        self._plans = {}
        self._subscriptions = {}
        self._next_plan_id = 1
        self._next_subscription_id = 1
        self.load_data() 

    def save_data(self):
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            
            data = {
                "plans": [
                    {
                        "plan_id": p.plan_id,
                        "name": p.name,
                        "price": p.price,
                        "duration_days": p.duration_days,
                        "is_active": p.is_active
                    } for p in self._plans.values()
                ],
                "subscriptions": [
                    {
                        "subscription_id": s.subscription_id,
                        "member_username": s.member_username,
                        "plan_id": s.plan_id,
                        "start_date": s.start_date.isoformat(),
                        "end_date": s.end_date.isoformat()
                    } for s in self._subscriptions.values()
                ]
            }
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        if not os.path.exists(self.file_path):
            return 
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            for p_data in data.get("plans", []):
                plan = SubscriptionPlan(
                    p_data["name"], p_data["price"], p_data["duration_days"],
                    plan_id=p_data["plan_id"], is_active=p_data["is_active"]
                )
                self._plans[plan.plan_id] = plan
                if plan.plan_id >= self._next_plan_id:
                    self._next_plan_id = plan.plan_id + 1
                    
            for s_data in data.get("subscriptions", []):
                sub = Subscription(
                    s_data["member_username"], s_data["plan_id"],
                    date.fromisoformat(s_data["start_date"]),
                    date.fromisoformat(s_data["end_date"]),
                    subscription_id=s_data["subscription_id"]
                )
                self._subscriptions[sub.subscription_id] = sub
                if sub.subscription_id >= self._next_subscription_id:
                    self._next_subscription_id = sub.subscription_id + 1
        except Exception as e:
            print(f"Error loading data: {e}")

    def add_plan(self, plan):
        if plan.plan_id is None:
            plan.plan_id = self._next_plan_id
            self._next_plan_id += 1
        self._plans[plan.plan_id] = plan
        self.save_data() 

    def get_plan_by_id(self, plan_id):
        return self._plans.get(plan_id)

    def add_subscription(self, subscription):
        if subscription.subscription_id is None:
            subscription.subscription_id = self._next_subscription_id
            self._next_subscription_id += 1
        self._subscriptions[subscription.subscription_id] = subscription
        self.save_data() 

    def get_subscriptions_by_username(self, username):
        return [sub for sub in self._subscriptions.values() if sub.member_username == username]
