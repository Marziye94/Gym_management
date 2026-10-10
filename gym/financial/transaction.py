from datetime import date

class Transaction:
    def __init__(self, transaction_type, amount, description, payment_id):
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.payment_id = payment_id

        today = date.today()
        self.date = f"{today.year}/{today.month}/{today.day}"
