import csv
import os

from gym.file_storage import write_files
from gym.payments.transaction import Transaction


DEFAULT_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "transactions.txt"))


class TransactionRepository:
    def __init__(self, file_path=DEFAULT_DATA_FILE):
        self.file_path = file_path

    def content_with(self, transaction):
        content = ""
        try:
            with open(self.file_path, "r", encoding="utf-8", newline="") as file:
                content = file.read()
        except FileNotFoundError:
            pass
        if content and not content.endswith("\n"):
            content += "\n"
        return content + transaction.to_text()

    def save(self, transaction):
        try:
            write_files([(self.file_path, self.content_with(transaction))])
            return True
        except (OSError, UnicodeError, AttributeError, TypeError):
            return False

    def load_all(self):
        transactions = []

        if not os.path.exists(self.file_path):
            return transactions

        try:
            with open(self.file_path, "r", encoding="utf-8", newline="") as file:
                for data in csv.reader(file, delimiter="|", strict=True):
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
        except (OSError, UnicodeError, csv.Error):
            raise OSError("Could not load transaction history.")

        return transactions

    def get_member_transactions(self, member_username):
        member_transactions = []
        transactions = self.load_all()

        for transaction in transactions:
            if transaction.member_username == member_username:
                member_transactions.append(transaction)

        return member_transactions
