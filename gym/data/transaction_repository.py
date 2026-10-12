import os
from gym.models.transaction import Transaction

class TransactionRepository:
    def __init__(self, file_path="transactions.txt"):
        self.file_path = file_path

    def save(self, transaction):
        try:
            with open(self.file_path, "a", encoding="utf-8") as file:
                file.write(transaction.to_text())
            return True

        except (OSError, AttributeError, TypeError):
            return False

    def load_all(self):
        transactions = []

        if not os.path.exists(self.file_path):
            return transactions

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split("|")
                    if len(data) != 6:
                        continue
                    try:
                        transaction = Transaction(
                            member_username=data[0],
                            transaction_type=data[1],
                            amount=data[2],
                            date=data[3],
                            description=data[4],
                            payment_id=data[5]
                        )

                        transactions.append(transaction)

                    except (ValueError, TypeError):
                        continue
        except OSError:
            return "Failed to read transactions"

        return transactions

    def get_member_transactions(self, member_username):
        member_transactions = []
        transactions = self.load_all()

        for transaction in transactions:
            if transaction.member_username == member_username:
                member_transactions.append(transaction)

        return member_transactions