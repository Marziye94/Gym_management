from datetime import date

def run_subscription_menu(manager, get_payments_callback):
    while True:
        print("\n--- Subscription Management ---")
        print("1. Register Subscription")
        print("2. View Payments")
        print("3. View Subscription Status")
        print("4. Back")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            username = input("Member username: ").strip()
            print("1. One Month\n2. Three Months\n3. Six Months")
            type_choice = input("Select type (1/2/3): ").strip()
            amount_input = input("Amount: ").strip()
            
            try:
                amount = float(amount_input)
                if type_choice == '1':
                    name, days = "One Month", 30
                elif type_choice == '2':
                    name, days = "Three Months", 90
                elif type_choice == '3':
                    name, days = "Six Months", 180
                else:
                    print("Invalid subscription type.")
                    continue
                    
                plan_result = manager.create_plan(name, amount, days)
                if plan_result.success:
                    sub_result = manager.create_subscription(username, plan_result.data.plan_id, date.today())
                    print(sub_result.message)
                else:
                    print(plan_result.message)
            except ValueError:
                print("Validation failed: Amount must be numeric.")
                
        elif choice == '2':
            payments = get_payments_callback()
            if not payments:
                print("No subscription payments found.")
            else:
                for p in payments:
                    print(f"Member: {p['member_name']} | Type: {p['subscription_type']} | "
                          f"Amount: {p['amount']} | Date: {p['payment_date']} | "
                          f"Start: {p['start_date']} | End: {p['end_date']} | Track ID: {p['tracking_number']}")
                          
        elif choice == '3':
            username = input("Member username: ").strip()
            status, info = manager.get_member_status(username, date.today())
            print(f"Status: {status}")
            if info:
                print(f"Details: {info}")
                
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")
