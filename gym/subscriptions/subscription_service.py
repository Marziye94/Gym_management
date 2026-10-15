import os
from datetime import date, timedelta
from uuid import uuid4

from gym.payments.transaction import Transaction
from gym.payments.transaction_repository import TransactionRepository

from gym.errors import StorageError
from gym.subscriptions.subscription import SubscriptionPlan, Subscription


class OperationResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data


class SubscriptionManager:
    def __init__(self, repository, is_member_active_lookup, transaction_repository=None):
        self.repo = repository
        self.is_member_active_lookup = is_member_active_lookup
        self.member_lookup = is_member_active_lookup
        if transaction_repository is None:
            transaction_repository = TransactionRepository(os.path.join(os.path.dirname(repository.file_path), "transactions.txt"))
        self.transaction_repository = transaction_repository

    def create_plan(self, name, price, duration_days):
        try:
            plan = SubscriptionPlan(name, price, duration_days)
            self.repo.add_plan(plan)
            return OperationResult(True, 'Plan created successfully.', plan)
        except (ValueError, OSError) as error:
            return OperationResult(False, str(error))

    def get_plan(self, plan_id):
        return self.repo.get_plan_by_id(plan_id)

    def list_plans(self):
        return self.repo.get_all_plans()

    def update_plan(self, plan_id, name, price, duration_days):
        plan = self.get_plan(plan_id)
        if plan is None:
            return OperationResult(False, 'Plan not found.')
        try:
            updated_plan = SubscriptionPlan(name, price, duration_days, plan_id, plan.is_active)
            self.repo.update_plan(updated_plan)
            return OperationResult(True, 'Plan updated successfully.', updated_plan)
        except (ValueError, OSError) as error:
            return OperationResult(False, str(error))

    def deactivate_plan(self, plan_id):
        plan = self.get_plan(plan_id)
        if plan is None:
            return OperationResult(False, 'Plan not found.')
        inactive_plan = SubscriptionPlan(plan.name, plan.price, plan.duration_days, plan_id, False)
        try:
            self.repo.update_plan(inactive_plan)
        except OSError as error:
            return OperationResult(False, str(error))
        return OperationResult(True, 'Plan deactivated successfully.', inactive_plan)

    def register_subscription(self, member_username, name, price, duration_days, start_date):
        try:
            member_username = self._active_member_username(member_username)
            if member_username is None:
                return OperationResult(False, 'Subscription failed: Member does not exist or is inactive.')
            plan = SubscriptionPlan(name, price, duration_days)
            subscription = Subscription(member_username, None, start_date,
                                        start_date + timedelta(days=duration_days))
            subscription.payment_id = uuid4().hex
            payment = Transaction(member_username, "subscription_payment", plan.price,
                                  subscription.payment_id, "Subscription: " + plan.name)
            self.repo.add_plan_and_subscription(plan, subscription, self.transaction_repository, payment)
            return OperationResult(True, 'Subscription created successfully.',
                                   self._subscription_info(subscription, plan))
        except (ValueError, TypeError, OverflowError, OSError, StorageError) as error:
            return OperationResult(False, str(error))

    def create_subscription(self, member_username, plan_id, start_date):
        try:
            member_username = self._active_member_username(member_username)
            if member_username is None:
                return OperationResult(False, 'Subscription failed: Member does not exist or is inactive.')
            plan = self.get_plan(plan_id)
            if plan is None or not plan.is_active:
                return OperationResult(False, 'Subscription failed: Plan not found or inactive.')
            end_date = start_date + timedelta(days=plan.duration_days)
            subscription = Subscription(member_username, plan_id, start_date, end_date)
            self.repo.add_subscription(subscription)
            return OperationResult(True, 'Subscription created successfully.', self._subscription_info(subscription, plan))
        except (ValueError, TypeError, OverflowError, OSError, StorageError) as error:
            return OperationResult(False, str(error))

    def renew_subscription(self, member_username, plan_id, current_date, payment_manager):
        try:
            if not isinstance(current_date, date):
                return OperationResult(False, 'A valid date is required.')
            member_username = self._active_member_username(member_username)
            if member_username is None:
                return OperationResult(False, 'Subscription failed: Member does not exist or is inactive.')
            plan = self.get_plan(plan_id)
            if plan is None or not plan.is_active:
                return OperationResult(False, 'Subscription failed: Plan not found or inactive.')
            start_date = current_date
            for previous in self.get_member_subscriptions(member_username):
                if previous.end_date > start_date:
                    start_date = previous.end_date
            subscription = Subscription(
                member_username, plan_id, start_date,
                start_date + timedelta(days=plan.duration_days),
            )
            subscription.payment_id = uuid4().hex
            success, message = payment_manager.pay_from_wallet(
                member_username, plan.price, 'Subscription: ' + plan.name, subscription.payment_id)
            if not success:
                return OperationResult(False, message)
            try:
                self.repo.add_subscription(subscription)
            except (OSError, TypeError, ValueError):
                refunded, refund_message = payment_manager.refund_to_wallet(
                    member_username, plan.price, 'Failed subscription purchase refund'
                )
                if not refunded:
                    return OperationResult(False, 'Subscription save failed; refund failed: ' + refund_message)
                return OperationResult(False, 'Subscription could not be saved. Wallet payment was refunded.')
            return OperationResult(True, 'Subscription purchased or renewed successfully.', self._subscription_info(subscription, plan))
        except (ValueError, TypeError, OverflowError, OSError, StorageError) as error:
            return OperationResult(False, str(error))

    def get_subscription(self, subscription_id):
        return self.repo.get_by_id(subscription_id)

    def get_member_subscriptions(self, member_username):
        return self.repo.get_subscriptions_by_username(member_username)

    def check_subscription(self, member_username, current_date):
        try:
            if not self.is_member_active_lookup(member_username):
                return OperationResult(False, 'Member does not exist or is inactive.')
            for subscription in self.get_member_subscriptions(member_username):
                if subscription.get_status(current_date) == 'Active':
                    return OperationResult(True, 'Active subscription found.', subscription)
        except (ValueError, TypeError, StorageError) as error:
            return OperationResult(False, str(error))
        return OperationResult(False, 'No active subscription found for this date.')

    def get_member_status(self, member_username, current_date):
        subscriptions = self.get_member_subscriptions(member_username)
        if not subscriptions:
            return 'No Subscription', None
        active_subscriptions = []
        for subscription in subscriptions:
            if subscription.get_status(current_date) == "Active":
                active_subscriptions.append(subscription)
        candidates = active_subscriptions if active_subscriptions else subscriptions
        latest = max(candidates, key=lambda subscription: subscription.end_date)
        status = latest.get_status(current_date)
        plan = self.get_plan(latest.plan_id)
        info = self._subscription_info(latest, plan)
        info['status'] = status
        return status, info

    def _subscription_info(self, subscription, plan):
        return {
            'member_username': subscription.member_username,
            'subscription_type': plan.name,
            'amount': plan.price,
            'start_date': subscription.start_date,
            'end_date': subscription.end_date,
        }

    def _active_member_username(self, username):
        member = self.is_member_active_lookup(username)
        if not member:
            return None
        if hasattr(member, "username"):
            return member.username
        return username.strip()

    def get_payment_subscription(self, payment_id):
        return self.repo.get_by_payment_id(payment_id)
