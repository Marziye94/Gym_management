from menus.member_menus.wallet_menu import wallet_menu
def member_menu(user, user_storage):
    if user.role != "Member" or not user.is_active:
        print("Only an active Member can enter this panel.")
        return
    print("Welcome, " + user.name + " (" + user.username + ")")
    while True:
        print("--- Member Panel ---")
        print("1. Profile and Subscription Status")
        print("2. Wallet")
        print("3. Classes")
        print("4. Workout Plan")
        print("5. Logout")

        choice = input("choose an option: ")

        if choice == "1":
            pass
        elif choice == "2":
            wallet_menu()
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")
