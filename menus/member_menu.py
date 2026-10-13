from menus.member_menus.wallet_menu import wallet_menu

def member_menu(member_username, payment_manager, subscription_manager):
    while True:
        print("--- Member Panel ---")
        print("1. Profile and Subscription Status")
        print("2. Wallet")
        print("3. Classes")
        print("4. Workout Plan")
        print("5. Exit")

        choice = input("choose an option: ")

        if choice == "1":
            pass
        elif choice == "2":
            wallet_menu(member_username, payment_manager, subscription_manager)
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")