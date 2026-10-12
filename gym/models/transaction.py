from datetime import datetime

class Transaction:
    def __init__(self, member_username,transaction_type, amount,payment_id, description="", date=None):
        self.member_username = member_username
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.payment_id = payment_id
        if date is None:
            self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_text(self):
        return (
            f"{self.username}|{self.transaction_type}|"
            f"{self.amount}|{self.date}|"
            f"{self.description}|{self.payment_id}\n"
        )
