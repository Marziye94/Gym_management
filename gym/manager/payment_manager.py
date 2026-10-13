from gym.data.wallet_repository import WalletRepository
from gym.data.transaction_repository import TransactionRepository
from gym.models.wallet import Wallet
from gym.models.transaction import Transaction

class PaymentManager:
    def __init__(self, wallet_repository, transaction_repository, bank_api):
        self.wallet_repository = wallet_repository
        self.transaction_repository = transaction_repository
        self.bank_api = bank_api

    @staticmethod
    def _validate_member(member_username):
        if not isinstance(member_username, str) or not member_username.strip():
            return None
        return True
    
    @staticmethod
    def _validate_amount(amount):
        if amount <= 0 or isinstance(amount, bool):
            return None
        try:
            amount = float(amount)
        except (ValueError,TypeError):
            return None
        return amount

    def get_wallet(self, member_username):
        if self._validate_member(member_username) is None:
            return False, "Invalid member username."
        
        wallet = self.wallet_repository.get_or_create_wallet(member_username)

        return wallet

    def get_balance(self, member_username):
        wallet = self.get_wallet(member_username)
        return wallet.get_balance()

    def charge_wallet(self, member_username, card, exp_month, exp_year, password, cvv2, amount):
        if not self._validate_member(member_username):
            return False, "Invalid member username."

        amount = self._validate_amount(amount)

        if amount is None:
            return False, "Amount must be a positive integer."

        wallet = self.get_wallet(member_username)

        try:
            payment_id = self.bank_api.pay(card, exp_month, exp_year, password, cvv2, amount)
        except (ValueError, TypeError):
            return False, "Invalid payment details."

        transaction = Transaction(
            member_username=member_username,
            transaction_type="wallet_charge",
            amount=amount,
            description="Wallet charge",
            payment_id=payment_id
        )

        if not self.transaction_repository.save(transaction):
            return False, "Transaction could not be saved. "
        
        wallet.increase_balance(amount)
        return True, "Wallet charged successfully."

    def pay_from_wallet(self, member_username, amount, description="Wallet payment"):
        if not self._validate_member(member_username):
            return False, "Invalid member username."

        amount = self._validate_amount(amount)

        if amount is None:
            return False, "Amount must be a positive integer."

        wallet = self.get_wallet(member_username)

        if amount > wallet.get_balance():
            return False, "Insufficient balance."

        payment_id = self.bank_api.generate_payment_id(amount, wallet.get_balance())

        transaction = Transaction(
            member_username=member_username,
            transaction_type="wallet_payment",
            amount=amount,
            description=description,
            payment_id=payment_id
        )
        if not self.transaction_repository.save(transaction):
            return False, "Transaction could not be saved. "

        wallet.decrease_balance(amount)
        return True, "Payment completed successfully."

    def get_member_transactions(self, member_username):
        if not self._validate_member(member_username):
            return []
        
        try:
            transactions = self.transaction_repository.get_member_transactions(member_username)
        except (OSError, ValueError, TypeError, AttributeError):
            return []

        if transactions is None:
            return []

        return transactions
