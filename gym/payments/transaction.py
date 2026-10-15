import csv
import io
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
        else:
            self.date = date

    def to_text(self):
        output = io.StringIO(newline="")
        writer = csv.writer(output, delimiter="|", lineterminator="\n")
        writer.writerow([self.member_username, self.transaction_type, self.amount,
                         self.date, self.description, self.payment_id])
        return output.getvalue()
