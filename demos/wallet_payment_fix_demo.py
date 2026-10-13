
import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, PROJECT_ROOT)

from gym.data.wallet_repository import WalletRepository
from gym.data.transaction_repository import TransactionRepository
from gym.manager.payment_manager import PaymentManager
from gym.financial.Bank import API


USERNAME = "reza123"

DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data"
)

TRANSACTION_FILE = os.path.join(
    DATA_DIR,
    "wallet_transactions_fix_demo.txt"
)
WALLET_FILE = os.path.join(DATA_DIR, "wallets_fix_demo.json")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Reset only the demo files.
    with open(TRANSACTION_FILE, "w", encoding="utf-8"):
        pass
    with open(WALLET_FILE, "w", encoding="utf-8") as file:
        file.write("{}")

    wallet_repository = WalletRepository(WALLET_FILE)
    transaction_repository = TransactionRepository(
        TRANSACTION_FILE
    )
    bank_api = API()

    payment_manager = PaymentManager(
        wallet_repository,
        transaction_repository,
        bank_api
    )

    print("=== Wallet and Payment Demo ===")

    # 1. Create or retrieve wallet
    print("\n1. Create wallet")

    wallet = payment_manager.get_wallet(USERNAME)
    print("Initial balance:", wallet.get_balance())

    # 2. Charge wallet
    print("\n2. Charge wallet")

    success, message = payment_manager.charge_wallet(
        USERNAME,
        "1234567890123456",
        6,
        1406,
        "123456",
        "123",
        1000000
    )

    print(message)

    # 3. Check balance after charge
    print("\n3. Balance after charge")

    balance = payment_manager.get_balance(USERNAME)
    print("Balance:", balance)

    # 4. Pay 300000
    print("\n4. Pay 300000")

    success, message = payment_manager.pay_from_wallet(
        USERNAME,
        300000
    )

    print(message)
    print("Remaining balance:", payment_manager.get_balance(USERNAME))

    # 5. Try to pay more than the balance
    print("\n5. Try to pay 800000")

    success, message = payment_manager.pay_from_wallet(
        USERNAME,
        800000
    )

    print(message)
    print("Balance:", payment_manager.get_balance(USERNAME))

    # 6. Try charging with invalid card details
    print("\n6. Try an invalid card")

    success, message = payment_manager.charge_wallet(
        USERNAME,
        "invalid-card",
        6,
        1406,
        "123456",
        "123",
        500000
    )

    print(message)
    print("Balance:", payment_manager.get_balance(USERNAME))

    # 7. Display transaction history
    print("\n7. Transaction history")

    success, transactions = payment_manager.get_member_transactions(
        USERNAME
    )

    if success:
        if len(transactions) == 0:
            print("No transactions found.")

        for transaction in transactions:
            print("--------------------")
            print("Type:", transaction.transaction_type)
            print("Amount:", transaction.amount)
            print("Date:", transaction.date)
            print("Description:", transaction.description)
            print("Tracking number:", transaction.payment_id)
    else:
        print("Could not load transaction history.")


if __name__ == "__main__":
    main()
