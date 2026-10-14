from datetime import date

def display_member_profile(authenticated_username, user_manager, subscription_manager):
    print("\n" + "="*30)
    print("        MEMBER PROFILE")
    print("="*30)
    
    user = user_manager.get_user(authenticated_username)
    if not user:
        print("Error: Account information not found.")
        return

    print(f"Name: {getattr(user, 'name', 'N/A')}")
    print(f"Username: {user.username}")
    print(f"Email: {getattr(user, 'email', 'N/A')}")
    print(f"Account Status: {'Active' if getattr(user, 'is_active', True) else 'Inactive'}")
    
    print("\n--- Subscription Status ---")
    status, info = subscription_manager.get_member_status(authenticated_username, date.today())
    
    print(f"Status: {status}")
    if info and status != "No Subscription":
        print(f"Type: {info.get('subscription_type', 'N/A')}")
        print(f"Start Date: {info.get('start_date', 'N/A')}")
        print(f"End Date: {info.get('end_date', 'N/A')}")
    print("==============================\n")
