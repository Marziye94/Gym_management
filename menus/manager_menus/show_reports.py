from gym.data.user_storage import UserStorage
from gym.data.class_repository import ClassRepository
from gym.data.transaction_repository import TransactionRepository
from gym.manager.report_manager import ReportManager


def create_default_report_manager():
    user_storage = UserStorage()
    class_repository = ClassRepository()
    transaction_repository = TransactionRepository()
    return ReportManager(user_storage, class_repository, transaction_repository)


def show_reports(report_manager=None):
    if report_manager is None:
        report_manager = create_default_report_manager()

    while True:
        print("\n--- Reports Menu ---")
        print("1. Active Members Count")
        print("2. Active Coaches Count")
        print("3. Active Classes Count")
        print("4. Total Revenue")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            result = report_manager.get_active_members_count()
            if result.success:
                print(f"Active Members: {result.data}")
            else:
                print(result.message)

        elif choice == "2":
            result = report_manager.get_active_coaches_count()
            if result.success:
                print(f"Active Coaches: {result.data}")
            else:
                print(result.message)

        elif choice == "3":
            result = report_manager.get_active_classes_count()
            if result.success:
                print(f"Active Classes: {result.data}")
            else:
                print(result.message)

        elif choice == "4":
            result = report_manager.get_total_revenue()
            if result.success:
                print(f"Total Revenue: {result.data}")
            else:
                print(result.message)

        elif choice == "5":
            return

        else:
            print("Invalid choice. Please try again.")


def show_reports_menu(report_manager=None):
    show_reports(report_manager)
