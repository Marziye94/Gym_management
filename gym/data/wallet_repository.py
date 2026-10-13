import json
import os
from gym.models.wallet import Wallet


class WalletRepository:
    def __init__(self, file_path="gym/data/wallets.json"):
        self.file_path = file_path
        self.wallets = {}
        self.load()

    def get_or_create_wallet(self, member_username):
        if member_username not in self.wallets:
            self.wallets[member_username] = Wallet(member_username)

        return self.wallets[member_username]
    
    def load(self):
        if not os.path.exists(self.file_path):
            self.wallets = {}
            return
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.wallets = {}

            for username, balance in data.items():
                wallet = Wallet(username, balance)
                self.wallets[username] = wallet

        except (OSError, TypeError, ValueError):
            raise ValueError("Could not load wallets")
        
    def save(self):
        data = {}

        for username, wallet in self.wallets.items():
            data[username] = wallet.get_balance()

        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file)

        except OSError:
            raise OSError("Could not save wallets")
