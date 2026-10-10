from bank import API


class Wallet:
    def __init__(self, member_username):
        self.__balance = 0
        self.member_username = member_username

    def deposit(self, amount):
        try:
            amount = int(amount)
        except ValueError:
            return "Amount must be an integer"
        else:
            if amount <= 0:
                return "Amount must be greater than zero"
            else:
                self.pay()

    def pay(self, amount, card, exp_month, exp_year, password, cvv2):
        try:
            api = API()
            payment_id = api.pay(card, exp_month, exp_year, password, cvv2)
            self.__balance += amount
        except ValueError:
            return "Invalid payment details."

    def withdraw(self, amount):
        try:
            amount = int(amount)
        except ValueError:
            return "Amount must be an integer"
        else:
            if amount <= 0:
                return "Amount must be greater than zero"
            elif amount > self.__balance:
                return "Insufficient balance"
            else:
                self.__balance -= amount

    def check_balance(self):
        return self.__balance
