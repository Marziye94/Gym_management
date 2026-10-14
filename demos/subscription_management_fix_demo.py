from datetime import date
import sys
import os

# اضافه کردن مسیر ریشه پروژه برای شناسایی پکیج gym
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from gym.models.subscription import SubscriptionPlan, Subscription
from gym.data.subscription_repository import SubscriptionRepository
from gym.manager.subscription_manager import SubscriptionManager

def mock_member_lookup(username):
    # شبیه‌سازی وضعیت کاربران طبق داکیومنت تسک
    members = {
        "reza123": True,       # موجود و فعال
        "sara123": True,       # موجود و فعال (بدون اشتراک)
        "inactive123": False   # موجود ولی غیرفعال
    }
    return members.get(username, False)

def run_demo():
    print("--- Starting Subscription Management Fix Demo ---\n")
    
    demo_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                            'demos', 'data', 'subscription_service_demo.json'))
    repo = SubscriptionRepository(demo_file)
    manager = SubscriptionManager(repo, mock_member_lookup)

    # 1. Create a One Month plan
    print("Step 1: Creating 'One Month' plan...")
    plan_result = manager.create_plan("One Month", 500000, 30)
    print(plan_result.message)
    plan_id = plan_result.data.plan_id

    # 2. Create subscription for reza123
    print("\nStep 2: Creating subscription for 'reza123' on 2026-10-12...")
    sub_result = manager.create_subscription("reza123", plan_id, date(2026, 10, 12))
    print(sub_result.message)
    if sub_result.success:
        print(f"Info: {sub_result.data}")

    # 3. Check reza123 on 2026-10-20 (Active)
    print("\nStep 3: Checking 'reza123' status on 2026-10-20...")
    status, info = manager.get_member_status("reza123", date(2026, 10, 20))
    print(f"Status: {status} | Details: {info}")

    # 4. Check reza123 on its end date (Expired)
    print("\nStep 4: Checking 'reza123' status on end date (2026-11-11)...")
    status, info = manager.get_member_status("reza123", date(2026, 11, 11))
    print(f"Status: {status} | Details: {info}")

    # 5. Check sara123 (No Subscription)
    print("\nStep 5: Checking 'sara123' status...")
    status, info = manager.get_member_status("sara123", date(2026, 10, 20))
    print(f"Status: {status}")

    # 6. Try to create a subscription for inactive123
    print("\nStep 6: Attempting subscription for 'inactive123'...")
    fail_result_1 = manager.create_subscription("inactive123", plan_id, date(2026, 10, 12))
    print(fail_result_1.message)

    # 7. Try an invalid amount and display a clear failure message
    print("\nStep 7: Attempting to create a plan with invalid amount ('Free')...")
    fail_result_2 = manager.create_plan("Invalid Plan", "Free", 30)
    print(fail_result_2.message)

if __name__ == "__main__":
    run_demo()