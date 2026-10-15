from gym.payments.wallet_repository import WalletRepository
from gym.payments.transaction_repository import TransactionRepository
from gym.payments.wallet import Wallet
from gym.payments.transaction import Transaction

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
        return Wallet._validate_amount(amount)

    def get_wallet(self, member_username):
        if self._validate_member(member_username) is None:
            raise ValueError("Invalid member username.")

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

        success, message = self._record_payment(wallet, transaction, True)
        if not success:
            return False, message
        return True, "Wallet charged successfully."


    def pay_from_wallet(self, member_username, amount, description="Wallet payment", payment_id=None):
        return self._pay_from_wallet(member_username, amount, description, transaction_type="wallet_payment", payment_id=payment_id)

    def pay_subscription_from_wallet(self, member_username, amount, plan_name, payment_id=None):
        return self._pay_from_wallet(member_username, amount, "Subscription: " + plan_name, transaction_type="subscription_payment", payment_id=payment_id)

    def _pay_from_wallet(self, member_username, amount, description, transaction_type, payment_id=None):
        if not self._validate_member(member_username):
            return False, "Invalid member username."

        amount = self._validate_amount(amount)

        if amount is None:
            return False, "Amount must be a positive number."

        wallet = self.get_wallet(member_username)

        if amount > wallet.get_balance():
            return False, "Insufficient balance."

        if payment_id is None:
            payment_id = self.bank_api.generate_payment_id(amount, wallet.get_balance())

        transaction = Transaction(
            member_username=member_username,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            payment_id=payment_id,
        )

        success, message = self._record_payment(wallet, transaction, False)

        if not success:
            return False, message

        return True, "Payment completed successfully."


    def get_member_transactions(self, member_username):
        if not self._validate_member(member_username):
            return False, []

        try:
            transactions = self.transaction_repository.get_member_transactions(member_username)
        except (OSError, ValueError, TypeError, AttributeError):
            return False, []

        if transactions is None:
            return False, []

        return True, transactions


    def refund_to_wallet(self, member_username, amount, description, transaction_type="wallet_refund"):
        amount = self._validate_amount(amount)

        if not self._validate_member(member_username) or amount is None:
            return False, "Invalid refund details."

        wallet = self.get_wallet(member_username)
        payment_id = self.bank_api.generate_payment_id(amount, wallet.get_balance())
        transaction = Transaction(
            member_username=member_username,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            payment_id=payment_id,
        )

        return self._record_payment(wallet, transaction, True)

    def _record_payment(self, wallet, transaction, is_charge):
        if is_charge:
            success, message = wallet.increase_balance(transaction.amount)
        else:
            success, message = wallet.decrease_balance(transaction.amount)
        if not success:
            return False, message
        try:
            self.wallet_repository.save()
        except (OSError, ValueError):
            self._undo_balance_change(wallet, transaction.amount, is_charge)
            return False, "Wallet balance could not be saved."
        if not self.transaction_repository.save(transaction):
            self._undo_balance_change(wallet, transaction.amount, is_charge)
            try:
                self.wallet_repository.save()
            except (OSError, ValueError):
                return False, "Transaction failed and wallet rollback could not be saved."
            return False, "Transaction could not be saved."
        return True, "Payment saved successfully."

    def _undo_balance_change(self, wallet, amount, is_charge):
        if is_charge:
            wallet.decrease_balance(amount)
        else:
            wallet.increase_balance(amount)
