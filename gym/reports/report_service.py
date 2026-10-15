class ReportResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data


class ReportManager:
    def __init__(self, user_storage, class_repository, transaction_repository):
        self.user_storage = user_storage
        self.class_repository = class_repository
        self.transaction_repository = transaction_repository

    def get_active_members_count(self):
        try:
            users = self.user_storage.load_users()
            count = 0
            for user in users:
                if user.role == "Member" and user.is_active == True:
                    count = count + 1
            return ReportResult(True, "Active members counted successfully.", count)
        except Exception as error:
            return ReportResult(False, "Could not calculate active members: " + str(error))

    def get_active_coaches_count(self):
        try:
            users = self.user_storage.load_users()
            count = 0
            for user in users:
                if user.role == "Coach" and user.is_active == True:
                    count = count + 1
            return ReportResult(True, "Active coaches counted successfully.", count)
        except Exception as error:
            return ReportResult(False, "Could not calculate active coaches: " + str(error))

    def get_active_classes_count(self):
        try:
            if not hasattr(self.class_repository, "get_all"):
                return ReportResult(False, "Class repository is not valid.")

            classes = self.class_repository.get_all()
            count = 0
            for gym_class in classes:
                if gym_class.is_active == True:
                    count = count + 1
            return ReportResult(True, "Active classes counted successfully.", count)
        except Exception as error:
            return ReportResult(False, "Could not calculate active classes: " + str(error))


    def get_total_revenue(self):
        try:
            transactions = self.transaction_repository.load_all()
            total_revenue = 0.0

            for tx in transactions:
                tx_type = str(tx.transaction_type).strip()
                description = str(tx.description).strip()

                try:
                    amount = float(tx.amount)
                except (ValueError, TypeError):
                    continue

                if amount <= 0:
                    continue

                if tx_type in ("wallet_charge", "wallet_refund"):
                    continue

                if tx_type == "subscription_payment_refund":
                    total_revenue -= amount
                    continue

                if tx_type == "subscription_payment":
                    total_revenue += amount
                    continue

                if (tx_type == "wallet_payment" and description.startswith("subscription: ")):
                    total_revenue += amount
                    continue

                if tx_type == "wallet_payment":
                    total_revenue += amount

            total_revenue = max(0.0, total_revenue)

            return ReportResult(True, "Total revenue calculated successfully.", total_revenue)

        except Exception as error:
            return ReportResult(False, "Could not calculate total revenue: " + str(error))