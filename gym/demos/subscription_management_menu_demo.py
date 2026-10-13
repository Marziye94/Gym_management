import sys
import os
import builtins
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gym.data.subscription_repository import SubscriptionRepository
from gym.manager.subscription_manager import SubscriptionManager
from menus.manager_menus.manage_subscriptions import run_subscription_menu

def mock_lookup(username):
    return username in ["reza123", "sara123"]

def mock_payments():
    return [{
        "member_name": "Reza",
        "subscription_type": "One Month",
        "amount": 500000,
        "payment_date": str(date.today()),
        "start_date": str(date.today()),
        "end_date": "2026-11-12",
        "tracking_number": "TRK-123456"
    }]

def run_demo():
    demo_json = "demos/data/subscriptions_demo.json"
    
    os.makedirs(os.path.dirname(demo_json), exist_ok=True)
    if os.path.exists(demo_json):
        os.remove(demo_json)
        
    repo = SubscriptionRepository(demo_json)
    manager = SubscriptionManager(repo, mock_lookup)
    
    input_sequence = ["1", "reza123", "1", "500000", "2", "3", "reza123", "3", "sara123", "4"]
    
    def fake_input(prompt=""):
        val = input_sequence.pop(0)
        print(f"{prompt}{val}")
        return val
        
    builtins.input = fake_input 
    
    print("--- Running Menu Demo ---\n")
    run_subscription_menu(manager, mock_payments)
    
    print("\n--- Verifying Persistence (JSON Load Test) ---")
    repo_reloaded = SubscriptionRepository(demo_json)
    subs = repo_reloaded.get_subscriptions_by_username("reza123")
    if subs:
        print(f"Success! Data for 'reza123' was securely restored from JSON.")
    else:
        print("Failed to restore data.")

if __name__ == "__main__":
    run_demo()