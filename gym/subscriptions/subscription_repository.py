import json
import os
from datetime import date

from gym.subscriptions.subscription import SubscriptionPlan, Subscription


DEFAULT_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'subscriptions.json'))


class SubscriptionRepository:
    def __init__(self, file_path=DEFAULT_DATA_FILE):
        self.file_path = os.fspath(file_path)
        self._plans = {}
        self._subscriptions = {}
        self._next_plan_id = 1
        self._next_subscription_id = 1
        self.load()

    def load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            return
        except (OSError, ValueError):
            raise ValueError('Could not load subscriptions.')
        try:
            plans = {}
            subscriptions = {}
            for record in data['plans']:
                plan = SubscriptionPlan(
                    name=record['name'],
                    price=record['price'],
                    duration_days=record['duration_days'],
                    plan_id=record['plan_id'],
                    is_active=record['is_active'],
                )
                if type(plan.plan_id) is not int or plan.plan_id < 1 or plan.plan_id in plans:
                    raise ValueError('Invalid plan ID.')
                plans[plan.plan_id] = plan
            for record in data['subscriptions']:
                subscription = Subscription(
                    member_username=record['member_username'],
                    plan_id=record['plan_id'],
                    start_date=date.fromisoformat(record['start_date']),
                    end_date=date.fromisoformat(record['end_date']),
                    subscription_id=record['subscription_id'],
                )
                if (
                    type(subscription.subscription_id) is not int
                    or subscription.subscription_id < 1
                    or subscription.subscription_id in subscriptions
                    or subscription.plan_id not in plans
                ):
                    raise ValueError('Invalid subscription record.')
                subscriptions[subscription.subscription_id] = subscription
        except (KeyError, TypeError, ValueError):
            raise ValueError('Invalid stored subscription data.')
        self._plans = plans
        self._subscriptions = subscriptions
        self._next_plan_id = max(plans, default=0) + 1
        self._next_subscription_id = max(subscriptions, default=0) + 1

    def save(self):
        plans = []
        for plan in self._plans.values():
            plans.append({
                'plan_id': plan.plan_id,
                'name': plan.name,
                'price': plan.price,
                'duration_days': plan.duration_days,
                'is_active': plan.is_active,
            })
        subscriptions = []
        for subscription in self._subscriptions.values():
            subscriptions.append({
                'subscription_id': subscription.subscription_id,
                'member_username': subscription.member_username,
                'plan_id': subscription.plan_id,
                'start_date': subscription.start_date.isoformat(),
                'end_date': subscription.end_date.isoformat(),
            })
        folder = os.path.dirname(os.path.abspath(self.file_path))
        os.makedirs(folder, exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({'plans': plans, 'subscriptions': subscriptions}, file, indent=2)

    def add_plan(self, plan):
        previous_plans = self._plans.copy()
        previous_id = self._next_plan_id
        if plan.plan_id is None:
            plan.plan_id = self._next_plan_id
            self._next_plan_id += 1
        self._plans[plan.plan_id] = plan
        try:
            self.save()
        except OSError:
            self._plans = previous_plans
            self._next_plan_id = previous_id
            raise

    def add_plan_and_subscription(self, plan, subscription):
        previous_plan_id = self._next_plan_id
        previous_subscription_id = self._next_subscription_id
        plan.plan_id = previous_plan_id
        subscription.plan_id = plan.plan_id
        subscription.subscription_id = previous_subscription_id
        self._plans[plan.plan_id] = plan
        self._subscriptions[subscription.subscription_id] = subscription
        self._next_plan_id += 1
        self._next_subscription_id += 1
        try:
            self.save()
        except OSError:
            del self._plans[plan.plan_id]
            del self._subscriptions[subscription.subscription_id]
            self._next_plan_id = previous_plan_id
            self._next_subscription_id = previous_subscription_id
            raise

    def get_plan_by_id(self, plan_id):
        return self._plans.get(plan_id)

    def get_all_plans(self):
        return list(self._plans.values())

    def update_plan(self, plan):
        previous_plan = self._plans[plan.plan_id]
        self._plans[plan.plan_id] = plan
        try:
            self.save()
        except OSError:
            self._plans[plan.plan_id] = previous_plan
            raise

    def add_subscription(self, subscription):
        previous_subscriptions = self._subscriptions.copy()
        previous_id = self._next_subscription_id
        if subscription.subscription_id is None:
            subscription.subscription_id = self._next_subscription_id
            self._next_subscription_id += 1
        self._subscriptions[subscription.subscription_id] = subscription
        try:
            self.save()
        except OSError:
            self._subscriptions = previous_subscriptions
            self._next_subscription_id = previous_id
            raise

    def get_subscriptions_by_username(self, username):
        subscriptions = []
        for subscription in self._subscriptions.values():
            if subscription.member_username == username:
                subscriptions.append(subscription)
        return subscriptions

    def get_by_id(self, subscription_id):
        return self._subscriptions.get(subscription_id)

    def get_by_member_username(self, username):
        return self.get_subscriptions_by_username(username)
