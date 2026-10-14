from datetime import date

from gym.data.errors import StorageError


def manage_subscriptions_menu(manager, get_payments_callback):
    while True:
        print("\n--- Subscription Management ---")
        print("1. Register Subscription")
        print("2. View Payments")
        print("3. View Subscription Status")
        print("4. Back")
        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                username = input("Member username: ").strip()
                print("1. One Month\n2. Three Months\n3. Six Months")
                type_choice = input("Select type (1/2/3): ").strip()
                if type_choice == "1":
                    name, days = "One Month", 30
                elif type_choice == "2":
                    name, days = "Three Months", 90
                elif type_choice == "3":
                    name, days = "Six Months", 180
                else:
                    print("Invalid subscription type.")
                    continue
                try:
                    amount = float(input("Amount: ").strip())
                except ValueError:
                    print("Amount must be numeric.")
                    continue
                result = manager.register_subscription(username, name, amount, days, date.today())
                print(result.message)
            elif choice == "2":
                found = False
                for payment in get_payments_callback():
                    if payment.transaction_type != "wallet_payment" or not payment.description.startswith("Subscription: "):
                        continue
                    found = True
                    print("Member:", payment.member_username,
                          "| Type:", payment.description.removeprefix("Subscription: "),
                          "| Amount:", payment.amount, "| Date:", payment.date,
                          "| Track ID:", payment.payment_id)
                if not found:
                    print("No subscription payments found.")
            elif choice == "3":
                username = input("Member username: ").strip()
                status, info = manager.get_member_status(username, date.today())
                print("Status:", status)
                if info:
                    print("Type:", info["subscription_type"], "| Amount:", info["amount"],
                          "| Start:", info["start_date"], "| End:", info["end_date"])
            elif choice == "4":
                return
            else:
                print("Invalid choice. Try again.")
        except (OSError, ValueError, StorageError) as error:
            print("Subscription operation failed:", error)
