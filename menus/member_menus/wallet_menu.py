from datetime import date

def wallet_menu(member_username, payment_manager, subscription_manager):
    
    while True:
        print("1. View Balance")
        print("2. Charge Wallet")
        print("3. View Transactions")
        print("4. Pay for / Renew Subscription")
        print("5. Back")

        choice = input("choose an option: ")

        if choice == "1":
            try:
                balance = payment_manager.get_balance(member_username)
                print(f"Your balance: {balance}")
            except (OSError, ValueError):
                print("Could not load balance")

        elif choice == "2":
            try:
                amount = float(input("Enter amount: "))

                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue

                card = input("Enter card number: ")
                exp_month = int(input("Enter expiry month: "))
                exp_year = int(input("Enter expiry year: "))
                password = input("Enter card password: ")
                cvv2 = input("Enter CVV2: ")

                success, message = payment_manager.charge_wallet(
                    member_username,
                    amount,
                    card,
                    exp_month,
                    exp_year,
                    password,
                    cvv2
                )

                print(message)

            except (ValueError, TypeError):
                print("Invalid input. Please enter valid numbers.")

        elif choice == "3":
            transactions = payment_manager.get_member_transactions(member_username)

            if not transactions:
                print("No transactions found.")
            else:
                for transaction in transactions:
                    print("--------------------")
                    print(f"Type: {transaction.transaction_type}")
                    print(f"Amount: {transaction.amount}")
                    print(f"Date: {transaction.date}")
                    print(f"Description: {transaction.description}")
                    print(f"Tracking number: {transaction.payment_id}")
        elif choice == "4":
            plans = subscription_manager.list_plans()
            active_plans = []

            for plan in plans:
                if plan.is_active:
                    active_plans.append(plan)

            if not active_plans:
                print("No active subscription plans available.")
                continue

            print("--- Available Subscription Plans ---")

            for plan in active_plans:
                print(
                    f"{plan.plan_id}. {plan.name} - "
                    f"Price: {plan.price} - "
                    f"Duration: {plan.duration_days} days"
                )

            try:
                plan_id = int(input("Enter plan ID: "))
            except ValueError:
                print("Invalid plan ID.")
                continue

            result = subscription_manager.renew_subscription(
                member_username,
                plan_id,
                date.today(),
                payment_manager
            )

            print(result.message)

        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")