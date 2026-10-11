from transaction import Transaction

class TransactionStorage:
    def __init__(self, file_name="transactions.txt"):
        self.file_name = file_name

    def save(self, transaction):
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(transaction.to_text())

    def get_transactions(self, username):
        transactions = []

        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split("|")

                    if len(data) != 6:
                        continue

                    if data[0] == username:
                        transactions.append(data)

        except FileNotFoundError:
            return []

        return transactions