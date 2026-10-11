from datetime import datetime

class Transaction:
    def __init__(self, username,transaction_type, amount, description, payment_id):
        self.username = username
        self.transaction_type = transaction_type
        self.amount = amount
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.description = description
        self.payment_id = payment_id

    def to_text(self):
        return (
            f"{self.username}|{self.transaction_type}|"
            f"{self.amount}|{self.date}|"
            f"{self.description}|{self.payment_id}\n"
        )
