from gym.models.gym_class import GymClass


class OperationResult:
    """کلاس استاندارد برای برگرداندن نتیجه عملیات‌ها"""

    def __init__(self, success: bool, message: str, data=None):
        self.success = success
        self.message = message
        self.data = data


class ClassManager:
    def __init__(self, repository, check_coach_active_fn, check_hall_active_fn):
        """
        مدیر کلاس‌ها.
        repository: آبجکت ClassRepository
        check_coach_active_fn: تابعی که نام مربی را می‌گیرد و True/False برمی‌گرداند
        check_hall_active_fn: تابعی که نام سالن را می‌گیرد و True/False برمی‌گرداند
        """
        self.repository = repository
        self.check_coach = check_coach_active_fn
        self.check_hall = check_hall_active_fn

    def create_class(self, name, exercise, coach_name, hall_name, schedule, capacity):
        try:
            # ۱. بررسی تکراری نبودن نام کلاس
            if self.repository.get_class(name):
                return OperationResult(False, f"کلاسی با نام '{name}' از قبل وجود دارد.")

            # ۲. بررسی وجود و فعال بودن مربی
            if not self.check_coach(coach_name):
                return OperationResult(False, f"مربی '{coach_name}' وجود ندارد یا غیرفعال است.")

            # ۳. بررسی وجود و فعال بودن سالنن
            if not self.check_hall(hall_name):
                return OperationResult(False, f"سالن '{hall_name}' وجود ندارد یا غیرفعال است.")

            # ۴. ساخت و ذخیره کلاس
            new_class = GymClass(name, exercise, coach_name,
                                 hall_name, schedule, capacity)
            self.repository.add(new_class)

            return OperationResult(True, "کلاس با موفقیت ایجاد شد.", new_class)

        except ValueError as e:
            # مدیریت خطاهای اعتبارسنجی (مثل ظرفیت صفر یا نام خالی)
            return OperationResult(False, str(e))
        except Exception as e:
            return OperationResult(False, f"خطای ناشناخته رخ داد: {str(e)}")

    def get_class(self, name):
        gym_class = self.repository.get_class(name)
        if gym_class:
            return OperationResult(True, "کلاس پیدا شد.", gym_class)
        return OperationResult(False, "کلاسی با این نام یافت نشد.")

    def list_classes(self):
        classes = self.repository.get_all()
        return OperationResult(True, f"{len(classes)} کلاس یافت شد.", classes)

    def update_class(self, original_name, new_name, exercise, schedule, capacity):
        try:
            gym_class = self.repository.get_class(original_name)
            if not gym_class:
                return OperationResult(False, "کلاس مورد نظر برای ویرایش یافت نشد.")

            # اگر اسم کلاس تغییر کرده، باید چک کنیم اسم جدید تکراری نباشد
            if original_name != new_name and self.repository.get_class(new_name):
                return OperationResult(False, f"کلاسی با نام جدید '{new_name}' از قبل وجود دارد.")

            gym_class.update_details(new_name, exercise, schedule, capacity)

            # اگر اسم تغییر کرده باشد، باید در دیتابیس هم کلید  جدید را جایگزین کنیم 
            if original_name != new_name:
                self.repository.classes.pop(original_name)
                self.repository.add(gym_class)
            else:
                self.repository.update(gym_class)

            return OperationResult(True, "اطلاعات کلاس با موفقیت به‌روزرسانی شد.", gym_class)
        except ValueError as e:
            return OperationResult(False, str(e))

    def assign_coach(self, class_name, coach_name):
        try:
            gym_class = self.repository.get_class(class_name)
            if not gym_class:
                return OperationResult(False, "کلاس یافت نشد.")

            if not self.check_coach(coach_name):
                return OperationResult(False, "مربی مورد نظر وجود ندارد یا غیرفعال است.")

            gym_class.assign_coach(coach_name)
            self.repository.update(gym_class)
            return OperationResult(True, f"مربی '{coach_name}' با موفقیت به کلاس اختصاص یافت.", gym_class)
        except ValueError as e:
            return OperationResult(False, str(e))

    def assign_hall(self, class_name, hall_name):
        try:
            gym_class = self.repository.get_class(class_name)
            if not gym_class:
                return OperationResult(False, "کلاس یافت نشد.")

            if not self.check_hall(hall_name):
                return OperationResult(False, "سالن مورد نظر وجود ندارد یا غیرفعال است.")

            gym_class.assign_hall(hall_name)
            self.repository.update(gym_class)
            return OperationResult(True, f"سالن '{hall_name}' با موفقیت به کلاس اختصاص یافت.", gym_class)
        except ValueError as e:
            return OperationResult(False, str(e))

    def deactivate_class(self, class_name):
        gym_class = self.repository.get_class(class_name)
        if not gym_class:
            return OperationResult(False, "کلاس یافت نشد.")

        gym_class.deactivate()
        self.repository.update(gym_class)
        return OperationResult(True, "کلاس با موفقیت غیرفعال شد.", gym_class)

    def activate_class(self, class_name):
        gym_class = self.repository.get_class(class_name)
        if not gym_class:
            return OperationResult(False, "کلاس یافت نشد.")

        gym_class.activate()
        self.repository.update(gym_class)
        return OperationResult(True, "کلاس با موفقیت فعال شد.", gym_class)
