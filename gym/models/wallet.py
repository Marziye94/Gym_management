import math


class Wallet:
    def __init__(self, member_username, balance=0):
        if not isinstance(member_username, str) or not member_username.strip():
            raise ValueError("Member username cannot be empty")
        self.member_username = member_username
        try:
            balance = float(balance)
        except (ValueError, TypeError):
            raise ValueError("Wallet balance must be a non-negative number.")
        if not math.isfinite(balance) or balance < 0:
            raise ValueError("Wallet balance must be a non-negative number.")
        self.__balance = balance

    @staticmethod
    def _validate_amount(amount):
        if isinstance(amount, bool):
            return None
        try:
            amount = float(amount)
        except (ValueError,TypeError):
            return None
        if not math.isfinite(amount) or amount <= 0:
            return None
        return amount


    def increase_balance(self, amount):
        amount = self._validate_amount(amount)
        if amount is None:
            return False, "Amount must be a valid positive number."

        self.__balance += amount
        return True, "Wallet balance increased successfully."

    def decrease_balance(self, amount):
        amount = self._validate_amount(amount)
        if amount is None:
            return False, "Amount must be a valid positive number."

        if amount > self.__balance:
            return False, "Insufficient balance"

        self.__balance -= amount
        return True, "Wallet balance decreased successfully."

    def check_balance(self):
        return f"Your wallet balance: {self.__balance}"

    def get_balance(self):
        return self.__balance


