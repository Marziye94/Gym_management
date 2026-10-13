from gym.models.wallet import Wallet


class WalletRepository:

    def __init__(self):
        self.wallets = {}

    def get_or_create_wallet(self, member_username):

        if member_username not in self.wallets:
            self.wallets[member_username] = Wallet(member_username)

        return self.wallets[member_username]