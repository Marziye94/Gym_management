from datetime import date

from gym.errors import StorageError

def show_subscription_payments(manager, payments, user_storage):
    found = False

    for payment in payments:
        description = str(payment.description).strip()
        is_subscription_payment = (payment.transaction_type == "subscription_payment")

        if (payment.transaction_type == "wallet_payment" and description.startswith("Subscription: ")):
            is_subscription_payment = True

        if not is_subscription_payment:
            continue

        found = True

        member = user_storage.get_user(payment.member_username)
        if member is not None:
            member_name = member.name
        else:
            member_name = payment.member_username

        subscription = manager.get_payment_subscription(payment.payment_id)

        plan_name = "Unknown"

        if description.startswith("Subscription: "):
            plan_name = description[len("Subscription: "):].strip()

        if subscription is not None:
            plan = manager.get_plan(subscription.plan_id)

            if plan is not None:
                plan_name = plan.name

            start_date = subscription.start_date
            end_date = subscription.end_date

        else:
            start_date = "Not recorded"
            end_date = "Not recorded"

        print("Member:", member_name)
        print("Plan:", plan_name)
        print("Amount:", payment.amount)
        print("Payment Date:", payment.date)
        print("Start Date:", start_date)
        print("End Date:", end_date)
        print("Tracking Number:", payment.payment_id)

    if not found:
        print("No subscription payments found.")

def manage_subscriptions_menu(manager, payment_manager, get_payments_callback, user_storage):
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

                show_subscription_payments(manager, payments, user_storage)

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
