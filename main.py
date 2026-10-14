from pathlib import Path

from gym.users.auth_service import AuthService
from gym.classes.class_repository import ClassRepository
from gym.enrollments.enrollment_repository import EnrollmentRepository
from gym.data.errors import StorageError
from gym.halls.hall_repository import HallRepository
from gym.subscriptions.subscription_repository import SubscriptionRepository
from gym.payments.transaction_repository import TransactionRepository
from gym.users.user_repository import UserStorage
from gym.payments.wallet_repository import WalletRepository
from gym.workouts.workout_plan_repository import WorkoutPlanRepository
from gym.payments.bank import API
from gym.classes.class_service import ClassManager
from gym.enrollments.enrollment_service import ClassEnrollmentManager
from gym.halls.hall_service import HallManager
from gym.payments.payment_service import PaymentManager
from gym.reports.report_service import ReportManager
from gym.subscriptions.subscription_service import SubscriptionManager
from gym.users.user_service import UserManager
from gym.workouts.workout_plan_service import WorkoutPlanManager
from menus.main_menu import main_menu


DEFAULT_DATA_DIRECTORY = Path(__file__).resolve().parent / "gym" / "data"


def load_repository(name, repository_class, file_path):
    try:
        repository = repository_class(file_path)
        if getattr(repository, "load_failed", False):
            print("Features using " + name + " are unavailable until the stored data is fixed.")
            return None
        return repository
    except (OSError, ValueError, TypeError, StorageError) as error:
        print("Could not load " + name + ": " + str(error))
        print("Features using this data are unavailable. The other menus remain available.")
        return None


def create_subscription_manager(user_storage, repository):
    def is_member_active(username):
        user = user_storage.get_user(username)
        return user is not None and user.role == "Member" and user.is_active

    return SubscriptionManager(repository, is_member_active)


def create_application(data_directory=DEFAULT_DATA_DIRECTORY):
    directory = Path(data_directory)
    users = load_repository("users", UserStorage, directory / "users.json")
    halls = load_repository("halls", HallRepository, directory / "halls.json")
    classes = load_repository("classes", ClassRepository, directory / "classes.json")
    subscriptions = load_repository("subscriptions", SubscriptionRepository, directory / "subscriptions.json")
    wallets = load_repository("wallets", WalletRepository, directory / "wallets.json")
    transactions = load_repository("transactions", TransactionRepository, directory / "transactions.txt")
    enrollments = load_repository("enrollments", EnrollmentRepository, directory / "enrollments.json")
    workouts = load_repository("workout plans", WorkoutPlanRepository, directory / "workout_plans.json")

    if users is not None:
        try:
            users.load_users()
        except StorageError as error:
            print("Could not load users:", error)
            users = None
    if transactions is not None:
        try:
            transactions.load_all()
        except OSError as error:
            print("Could not load transactions:", error)
            transactions = None

    auth = AuthService(users) if users is not None else None
    user_manager = UserManager(None, users) if users is not None else None
    hall_manager = HallManager(halls) if halls is not None else None
    subscription_manager = None
    if users is not None and subscriptions is not None:
        subscription_manager = create_subscription_manager(users, subscriptions)

    def check_coach(username):
        coach = users.get_user(username)
        return coach is not None and coach.role == "Coach" and coach.is_active

    def check_hall(name):
        hall = hall_manager.get_hall(name)
        return hall is not None and hall.is_active

    class_manager = None
    if classes is not None and users is not None and hall_manager is not None:
        class_manager = ClassManager(classes, check_coach, check_hall)
    payment_manager = None
    if wallets is not None and transactions is not None:
        payment_manager = PaymentManager(wallets, transactions, API())
    enrollment_manager = None
    if enrollments is not None and classes is not None and subscription_manager is not None:
        enrollment_manager = ClassEnrollmentManager(enrollments, classes, users, subscription_manager)
    workout_manager = None
    if workouts is not None and classes is not None and enrollments is not None:
        workout_manager = WorkoutPlanManager(workouts, classes, enrollments)
    report_manager = None
    if users is not None and classes is not None and transactions is not None:
        report_manager = ReportManager(users, classes, transactions)

    return {
        "user_storage": users,
        "hall_repository": halls,
        "class_repository": classes,
        "subscription_repository": subscriptions,
        "wallet_repository": wallets,
        "transaction_repository": transactions,
        "enrollment_repository": enrollments,
        "workout_repository": workouts,
        "auth": auth,
        "user_manager": user_manager,
        "hall_manager": hall_manager,
        "class_manager": class_manager,
        "subscription_manager": subscription_manager,
        "payment_manager": payment_manager,
        "enrollment_manager": enrollment_manager,
        "workout_manager": workout_manager,
        "report_manager": report_manager,
    }


def main():
    main_menu(create_application())


if __name__ == "__main__":
    main()
