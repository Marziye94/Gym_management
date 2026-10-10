from transaction import Transaction

class TransactionList:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_all_transactions(self):
        return self.transactions


# transaction = Transaction("deposit", amount, "successful deposit", payment_id)
# transactions = TransactionList()
# transactions.add_transaction(transaction)