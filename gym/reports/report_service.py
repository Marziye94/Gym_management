import math


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
            total_revenue = 0

            for tx in transactions:
                tx_type = str(getattr(tx, "transaction_type", "")
                              ).strip().lower()
                pay_id = str(getattr(tx, "payment_id", "")).strip().lower()
                amount_raw = getattr(tx, "amount", 0)

                if pay_id == "" or pay_id == "none" or "fail" in pay_id:
                    continue
                if tx_type not in ("wallet_payment", "subscription_payment", "wallet_refund", "subscription_payment_refund"):
                    continue

                try:
                    amount_val = float(amount_raw)
                    if math.isfinite(amount_val) and amount_val > 0:
                        if tx_type in ("wallet_refund", "subscription_payment_refund"):
                            total_revenue -= amount_val
                        else:
                            total_revenue += amount_val
                except (ValueError, TypeError):
                    continue

            return ReportResult(True, "Total revenue calculated successfully.", max(0.0, total_revenue))
        except Exception as error:
            return ReportResult(False, "Could not calculate total revenue: " + str(error))
