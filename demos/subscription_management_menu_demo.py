"""Run the real subscription menu with separate demo-only data."""
import os
import sys
from datetime import date

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from gym.users.auth_service import AuthService
from gym.subscriptions.subscription_repository import SubscriptionRepository
from gym.payments.transaction_repository import TransactionRepository
from gym.users.user_repository import UserStorage
from gym.payments.wallet_repository import WalletRepository
from gym.payments.bank import API
from gym.payments.payment_service import PaymentManager
from gym.application import create_subscription_manager
from gym.subscriptions.subscription_menu import manage_subscriptions_menu

DATA_DIR = os.path.join(PROJECT_ROOT, "demos", "data")


def run_demo():
    os.makedirs(DATA_DIR, exist_ok=True)
    users = UserStorage(os.path.join(DATA_DIR, "subscription_menu_users.json"))
    subscriptions_path = os.path.join(DATA_DIR, "subscription_menu_subscriptions.json")
    transactions_path = os.path.join(DATA_DIR, "subscription_menu_transactions.txt")
    wallets_path = os.path.join(DATA_DIR, "subscription_menu_wallets.json")
    users.save_users([])
    for path, content in ((subscriptions_path, '{"plans": [], "subscriptions": []}'),
                          (transactions_path, ""), (wallets_path, "{}")):
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
    auth = AuthService(users)
    for name, username in (("Reza", "reza123"), ("Sara", "sara123")):
        result = auth.register_user(name, username, "Member123@", "Member")
        if not result["success"]:
            print(result["message"])
            return
    repository = SubscriptionRepository(subscriptions_path)
    transactions = TransactionRepository(transactions_path)
    manager = create_subscription_manager(users, repository, transactions)
    payments = PaymentManager(WalletRepository(wallets_path), transactions, API())
    plan_result = manager.create_plan("One Month", 5000, 30)
    if not plan_result.success:
        print(plan_result.message)
        return
    success, message = payments.charge_wallet("reza123", "1234567890123456", 12,
                                            1408, "123456", "123", 10000)
    if not success:
        print(message)
        return
    result = manager.renew_subscription("reza123", plan_result.data.plan_id, date.today(), payments)
    print(result.message)
    if not result.success:
        return
    print("Demo members: reza123 and sara123. Reza already has a paid subscription.")
    manage_subscriptions_menu(manager, payments, transactions.load_all)
    reloaded = create_subscription_manager(users, SubscriptionRepository(subscriptions_path))
    status, info = reloaded.get_member_status("reza123", date.today())
    print("Reloaded Reza subscription:", status, info)


if __name__ == "__main__":
    run_demo()
