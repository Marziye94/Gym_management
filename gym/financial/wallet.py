from bank import API
from transaction import Transaction
from transaction_storage import TransactionStorage


class Wallet:
    def __init__(self, member_username):
        self.__balance = 0
        self.api = API()
        self.transaction_storage = TransactionStorage()
        self.member_username = member_username

    def deposit(self, card, exp_month, exp_year, password, cvv2, amount):
        try:
            amount = int(amount)
        except ValueError:
            return False, "Amount must be an integer"

        if amount <= 0:
            return False, "Amount must be greater than zero"

        try:
            payment_id = self.api.pay(card, exp_month, exp_year, password, cvv2, amount)

        except ValueError:
            return False, "Invalid payment details."

        transaction = Transaction(
            username=self.username,
            transaction_type="deposit",
            amount=amount,
            description="Wallet top-up",
            payment_id=payment_id
        )

        if not self.transaction_storage.save(transaction):
            return False, "Could not save transaction."

        self.balance += amount
        return True, "Wallet charged successfully. "


    def withdraw(self, amount):
        try:
            amount = int(amount)
        except ValueError:
            return False, "Amount must be an integer"
    
        if amount <= 0:
            return False, "Amount must be greater than zero"
        elif amount > self.__balance:
            return False, "Insufficient balance"
        
        payment_id = self.api.generate_payment_id(amount, 0)
        transaction = Transaction(
            username=self.username,
            transaction_type="withdrawal",
            amount=amount,
            description="wallet withdrawal",
            payment_id=payment_id
            )

        if not self.transaction_storage.save(transaction):
            return False, "Could not save transaction."
    
        self.__balance -= amount
        return True, "Withdraw Successful"

    def check_balance(self):
        return f"Your wallet balance: {self.__balance}"

