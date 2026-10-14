import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gym.data.user_storage import UserStorage
from gym.classes.class_repository import ClassRepository
from gym.data.transaction_repository import TransactionRepository
from gym.manager.report_manager import ReportManager
from gym.models.user import User
from gym.classes.gym_class import GymClass
from gym.models.transaction import Transaction


def run_reports_demo():
    demo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "reports_demo")
    os.makedirs(demo_dir, exist_ok=True)

    users_file = os.path.join(demo_dir, "users_demo.json")
    classes_file = os.path.join(demo_dir, "classes_demo.json")
    transactions_file = os.path.join(demo_dir, "transactions_demo.txt")

    for file_path in (users_file, classes_file, transactions_file):
        if os.path.exists(file_path):
            os.remove(file_path)

    user_storage = UserStorage(data_file=users_file)
    class_repository = ClassRepository(data_file=classes_file)
    transaction_repository = TransactionRepository(file_path=transactions_file)

    demo_users = [
        User(1, "Ali Rezaei", "ali_member", "Pass@1234", "Member", is_active=True),
        User(2, "Mina Karimi", "mina_member", "Pass@1234", "Member", is_active=True),
        User(3, "Omid Moradi", "omid_member", "Pass@1234", "Member", is_active=False),
        User(4, "Sara Ahmadi", "sara_coach", "Pass@1234", "Coach", is_active=True),
        User(5, "Reza Hosseini", "reza_coach", "Pass@1234", "Coach", is_active=False),
    ]
    user_storage.save_users(demo_users)

    class_1 = GymClass("Morning Yoga", "Yoga", "Sara Ahmadi", "Main Hall", "Saturday", "10:00", 15, is_active=True)
    class_2 = GymClass("Evening Fitness", "Fitness", "Sara Ahmadi", "Studio Hall", "Sunday", "18:00", 20, is_active=True)
    class_3 = GymClass("Night CrossFit", "CrossFit", "Sara Ahmadi", "Main Hall", "Monday", "20:00", 12, is_active=False)

    class_repository.add(class_1)
    class_repository.add(class_2)
    class_repository.add(class_3)


    tx_1 = Transaction("ali_member", "wallet_charge", 1000000, "PAY-1001", "Wallet charge")
    tx_2 = Transaction("ali_member", "subscription_payment", 500000, "PAY-1002", "Subscription payment")
    tx_3 = Transaction("mina_member", "subscription_payment", 300000, "PAY-1003", "Subscription payment")
    tx_4 = Transaction("omid_member", "subscription_payment", 400000, "FAILED", "Failed subscription payment")

    transaction_repository.save(tx_1)
    transaction_repository.save(tx_2)
    transaction_repository.save(tx_3)
    transaction_repository.save(tx_4)

  
    report_manager = ReportManager(user_storage, class_repository, transaction_repository)

    print(f"Active Members: {report_manager.get_active_members_count().data}")
    print(f"Active Coaches: {report_manager.get_active_coaches_count().data}")
    print(f"Active Classes: {report_manager.get_active_classes_count().data}")
    print(f"Total Revenue: {report_manager.get_total_revenue().data}")


if __name__ == "__main__":
    run_reports_demo()