
import os
import json
from datetime import date

import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from gym.models.wallet import Wallet
from gym.models.subscription import SubscriptionPlan, Subscription
from gym.data.wallet_repository import WalletRepository
from gym.data.transaction_repository import TransactionRepository
from gym.data.subscription_repository import SubscriptionRepository
from gym.manager.payment_manager import PaymentManager
from gym.manager.subscription_manager import SubscriptionManager
from gym.financial.bank import API


DEMO_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DEMO_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

WALLET_FILE = os.path.join(DATA_DIR, "wallets.json")
TRANSACTION_FILE = os.path.join(DATA_DIR, "transactions.txt")
SUBSCRIPTION_FILE = os.path.join(DATA_DIR, "subscriptions.json")

MEMBER_USERNAME = "demo_member"


# Wallet that saves its balance in the demo folder
class DemoWallet(Wallet):
    def __init__(self, member_username, repository, balance=0):
        super().__init__(member_username)
        self.repository = repository

        if balance > 0:
            super().increase_balance(balance)

    def increase_balance(self, amount):
        success, message = super().increase_balance(amount)

        if success:
            self.repository.save()

        return success, message

    def decrease_balance(self, amount):
        success, message = super().decrease_balance(amount)

        if success:
            self.repository.save()

        return success, message


class DemoWalletRepository(WalletRepository):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.balances = {}

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    self.balances = json.load(file)
            except (OSError, ValueError):
                self.balances = {}

    def get_or_create_wallet(self, member_username):
        if member_username not in self.wallets:
            balance = self.balances.get(member_username, 0)

            wallet = DemoWallet(
                member_username,
                self,
                int(balance)
            )

            self.wallets[member_username] = wallet

        return self.wallets[member_username]

    def save(self):
        for username, wallet in self.wallets.items():
            self.balances[username] = wallet.get_balance()

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.balances, file, indent=4)


# Subscription repository that saves demo data
class DemoSubscriptionRepository(SubscriptionRepository):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.load()

    def load(self):
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, ValueError):
            return

        for item in data.get("plans", []):
            plan = SubscriptionPlan(
                item["name"],
                item["price"],
                item["duration_days"],
                item["plan_id"],
                item["is_active"]
            )

            self.plans[plan.plan_id] = plan

        for item in data.get("subscriptions", []):
            subscription = Subscription(
                item["member_username"],
                item["plan_id"],
                date.fromisoformat(item["start_date"]),
                date.fromisoformat(item["end_date"]),
                item["subscription_id"],
                item["status"]
            )

            self.subscriptions[subscription.subscription_id] = subscription

        if self.plans:
            self.next_plan_id = max(self.plans) + 1

        if self.subscriptions:
            self.next_subscription_id = max(self.subscriptions) + 1

    def save(self):
        data = {
            "plans": [],
            "subscriptions": []
        }

        for plan in self.plans.values():
            data["plans"].append({
                "plan_id": plan.plan_id,
                "name": plan.name,
                "price": plan.price,
                "duration_days": plan.duration_days,
                "is_active": plan.is_active
            })

        for sub in self.subscriptions.values():
            data["subscriptions"].append({
                "subscription_id": sub.subscription_id,
                "member_username": sub.member_username,
                "plan_id": sub.plan_id,
                "start_date": sub.start_date.isoformat(),
                "end_date": sub.end_date.isoformat(),
                "status": sub.status
            })

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_plan(self, plan):
        super().add_plan(plan)
        self.save()

    def update_plan(self, plan):
        super().update_plan(plan)
        self.save()

    def add(self, subscription):
        super().add(subscription)
        self.save()

    def update(self, subscription):
        super().update(subscription)
        self.save()


def member_lookup(username):
    return username == MEMBER_USERNAME


def show_transactions(payment_manager):
    transactions = payment_manager.get_member_transactions(
        MEMBER_USERNAME
    )

    if not transactions:
        print("No transactions found.")
        return

    print("\n--- Transaction History ---")

    for transaction in transactions:
        print(
            f"Type: {transaction.transaction_type} | "
            f"Amount: {transaction.amount} | "
            f"Date: {transaction.date} | "
            f"Description: {transaction.description}"
        )


def main():
    print("=== Wallet and Subscription Demo ===")

    # Create repositories using demo-only files
    wallet_repository = DemoWalletRepository(WALLET_FILE)

    transaction_repository = TransactionRepository(
        TRANSACTION_FILE
    )

    subscription_repository = DemoSubscriptionRepository(
        SUBSCRIPTION_FILE
    )

    bank_api = API()

    payment_manager = PaymentManager(
        wallet_repository,
        transaction_repository,
        bank_api
    )

    subscription_manager = SubscriptionManager(
        subscription_repository,
        member_lookup
    )

    # Create the demo plan if it does not already exist
    plan = None

    for existing_plan in subscription_manager.list_plans():
        if existing_plan.name == "Demo Monthly Plan":
            plan = existing_plan
            break

    if plan is None:
        result = subscription_manager.create_plan(
            "Demo Monthly Plan",
            5000,
            30
        )

        if not result.success:
            print(result.message)
            return

        plan = result.data

    # Step 1: Charge the wallet
    print("\n--- Step 1: Charge Wallet ---")

    success, message = payment_manager.charge_wallet(
        MEMBER_USERNAME,
        "1234567890123456",
        12,
        1408,
        "123456",
        "123",
        10000
    )

    print(message)

    if not success:
        return

    print("Balance:", payment_manager.get_balance(MEMBER_USERNAME))

    # Step 2: Purchase a subscription
    print("\n--- Step 2: Purchase Subscription ---")

    success, message = payment_manager.pay_from_wallet(
        MEMBER_USERNAME,
        plan.price,
        "Subscription purchase"
    )

    print(message)

    if not success:
        return

    result = subscription_manager.create_subscription(
        MEMBER_USERNAME,
        plan.plan_id,
        date.today()
    )

    print(result.message)

    if not result.success:
        print(
            "Payment was completed, but subscription creation failed."
        )
        return

    print("Balance:", payment_manager.get_balance(MEMBER_USERNAME))

    # Step 3: Display transaction history
    print("\n--- Step 3: View Transactions ---")
    show_transactions(payment_manager)

    # Step 4: Reload data using new repository objects
    print("\n--- Step 4: Reload Saved Data ---")

    reloaded_wallet_repository = DemoWalletRepository(WALLET_FILE)

    reloaded_transaction_repository = TransactionRepository(
        TRANSACTION_FILE
    )

    reloaded_subscription_repository = DemoSubscriptionRepository(
        SUBSCRIPTION_FILE
    )

    reloaded_payment_manager = PaymentManager(
        reloaded_wallet_repository,
        reloaded_transaction_repository,
        API()
    )

    reloaded_subscription_manager = SubscriptionManager(
        reloaded_subscription_repository,
        member_lookup
    )

    print(
        "Reloaded wallet balance:",
        reloaded_payment_manager.get_balance(MEMBER_USERNAME)
    )

    print("\nReloaded transaction history:")
    show_transactions(reloaded_payment_manager)

    print("\nReloaded subscriptions:")

    subscriptions = (
        reloaded_subscription_manager.get_member_subscriptions(
            MEMBER_USERNAME
        )
    )

    if not subscriptions:
        print("No subscriptions found.")
    else:
        for sub in subscriptions:
            plan = reloaded_subscription_manager.get_plan(sub.plan_id)

            print(
                f"Plan: {plan.name} | "
                f"Start: {sub.start_date} | "
                f"End: {sub.end_date} | "
                f"Status: {sub.status}"
            )

    print("\n=== Demo Finished ===")


if __name__ == "__main__":
    main()