"""Demonstrate wallet and subscription persistence with demo-only files."""
import os
import sys
from datetime import date

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from gym.payments.wallet_repository import WalletRepository
from gym.payments.transaction_repository import TransactionRepository
from gym.subscriptions.subscription_repository import SubscriptionRepository
from gym.payments.payment_service import PaymentManager
from gym.subscriptions.subscription_service import SubscriptionManager
from gym.payments.bank import API


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
WALLET_FILE = os.path.join(DATA_DIR, 'wallets.json')
TRANSACTION_FILE = os.path.join(DATA_DIR, 'transactions.txt')
SUBSCRIPTION_FILE = os.path.join(DATA_DIR, 'subscriptions.json')
MEMBER_USERNAME = 'demo_member'


def member_lookup(username):
    return username == MEMBER_USERNAME


def show_transactions(payment_manager):
    success, transactions = payment_manager.get_member_transactions(MEMBER_USERNAME)
    if not success:
        print('Could not load transaction history.')
        return
    if not transactions:
        print('No transactions found.')
        return
    for transaction in transactions:
        print('Type:', transaction.transaction_type)
        print('Amount:', transaction.amount)
        print('Date:', transaction.date)
        print('Description:', transaction.description)
        print('Tracking number:', transaction.payment_id)


def main():
    print('=== Wallet and Subscription Demo ===')
    os.makedirs(DATA_DIR, exist_ok=True)
    for path, content in (
        (WALLET_FILE, '{}'),
        (TRANSACTION_FILE, ''),
        (SUBSCRIPTION_FILE, '{"plans": [], "subscriptions": []}'),
    ):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)

    wallets = WalletRepository(WALLET_FILE)
    transactions = TransactionRepository(TRANSACTION_FILE)
    subscriptions = SubscriptionRepository(SUBSCRIPTION_FILE)
    payment_manager = PaymentManager(wallets, transactions, API())
    subscription_manager = SubscriptionManager(subscriptions, member_lookup)
    result = subscription_manager.create_plan('Demo Monthly Plan', 5000, 30)
    if not result.success:
        print(result.message)
        return
    plan = result.data

    print('\n--- Step 1: Charge Wallet ---')
    success, message = payment_manager.charge_wallet(
        MEMBER_USERNAME, '1234567890123456', 12, 1408, '123456', '123', 10000
    )
    print(message)
    if not success:
        return
    print('Balance:', payment_manager.get_balance(MEMBER_USERNAME))

    print('\n--- Step 2: Purchase Subscription ---')
    result = subscription_manager.renew_subscription(
        MEMBER_USERNAME, plan.plan_id, date.today(), payment_manager
    )
    print(result.message)
    if not result.success:
        return
    print('Balance:', payment_manager.get_balance(MEMBER_USERNAME))

    print('\n--- Step 3: View Transactions ---')
    show_transactions(payment_manager)

    print('\n--- Step 4: Reload Saved Data ---')
    reloaded_payment = PaymentManager(
        WalletRepository(WALLET_FILE), TransactionRepository(TRANSACTION_FILE), API()
    )
    reloaded_subscriptions = SubscriptionManager(
        SubscriptionRepository(SUBSCRIPTION_FILE), member_lookup
    )
    print('Reloaded wallet balance:', reloaded_payment.get_balance(MEMBER_USERNAME))
    show_transactions(reloaded_payment)
    for subscription in reloaded_subscriptions.get_member_subscriptions(MEMBER_USERNAME):
        plan = reloaded_subscriptions.get_plan(subscription.plan_id)
        print('Plan:', plan.name)
        print('Start:', subscription.start_date)
        print('End:', subscription.end_date)
        print('Status:', subscription.get_status(date.today()))
    print('\n=== Demo Finished ===')


if __name__ == '__main__':
    main()
