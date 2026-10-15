from datetime import date

from gym.errors import StorageError


def manage_subscriptions_menu(manager, payment_manager, get_payments_callback):
    while True:
        print("--- Subscription Management ---")
        print("1. Create Subscription Plan")
        print("2. View Subscription Plans")
        print("3. Register Subscription for Member")
        print("4. View Payments")
        print("5. View Subscription Status")
        print("6. Back")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Plan name: ").strip()
                try:
                    price = float(input("Plan price: ").strip())
                    duration_days = int(input("Duration in days: ").strip())
                except ValueError:
                    print("Price must be numeric and duration must be an integer.")
                    continue

                result = manager.create_plan(name, price, duration_days)
                print(result.message)

            elif choice == "2":
                plans = manager.list_plans()

                if not plans:
                    print("No subscription plans found.")
                    continue

                print("--- Subscription Plans ---")
                for plan in plans:
                    print(
                        f"ID: {plan.plan_id} | "
                        f"Name: {plan.name} | "
                        f"Price: {plan.price} | "
                        f"Duration: {plan.duration_days} days | "
                    )

            elif choice == "3":
                username = input("Member username: ").strip()
                plans = manager.list_plans()

                if not plans:
                    print("No subscription plans available.")
                    continue

                print("-- Available Subscription Plans ---")
                for plan in plans:
                    print(
                        f"ID: {plan.plan_id} | "
                        f"Name: {plan.name} | "
                        f"Price: {plan.price} | "
                        f"Duration: {plan.duration_days} days"
                    )

                try:
                    plan_id = int(input("Select plan ID: ").strip())
                except ValueError:
                    print("Plan ID must be an integer.")
                    continue

                result = manager.assign_subscription(username, plan_id, date.today(), payment_manager)
                print(result.message)

            elif choice == "4":
                payments = get_payments_callback()
                found = False

                for payment in payments:
                    description = str(payment.description).strip()
                    found = True

                    plan_name = description
                    if plan_name.startswith("Subscription: "):
                        plan_name = plan_name.removeprefix(
                            "Subscription: ")

                    print(
                        "Member:", payment.member_username,
                        "| Plan:", plan_name,
                        "| Amount:", payment.amount,
                        "| Date:", payment.date,
                        "| Tracking ID:", payment.payment_id,
                    )

                if not found:
                    print("No subscription payments found.")

            elif choice == "5":
                username = input("Member username: ").strip()
                status, info = manager.get_member_status(username, date.today())

                print("Status:", status)

                if info:
                    print(
                        "Plan:", info["subscription_type"],
                        "| Price:", info["amount"],
                        "| Start:", info["start_date"],
                        "| End:", info["end_date"],
                    )

            elif choice == "6":
                return

            else:
                print("Invalid choice. Please try again.")

        except (OSError, ValueError, TypeError, StorageError) as error:
            print("Subscription operation failed:", error)
