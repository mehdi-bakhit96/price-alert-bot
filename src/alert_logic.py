from typing import Optional, Dict, Any, Tuple

class AlertEngine:
    @staticmethod
    def evaluate(current: Dict[str, Any], previous: Optional[Dict[str, Any]], drop_threshold_percent: float) -> Tuple[bool, str]:
        """
        بررسی شروط هشدار.
        خروجی: (آیا هشدار فعال شود؟ , متن دلیل هشدار)
        """
        if not previous:
            return False, "اولین بار است که محصول ثبت می‌شود (حالت پایه)."

        alerts = []
        old_price = previous.get("price", 0.0)
        new_price = current.get("price", 0.0)
        old_stock = previous.get("stock", 0)
        new_stock = current.get("stock", 0)

        # ۱. بررسی افت قیمت
        if old_price > 0 and new_price < old_price:
            drop_percent = ((old_price - new_price) / old_price) * 100
            if drop_percent >= drop_threshold_percent:
                alerts.append(f"🔻 **افت قیمت ({drop_percent:.1f}%)**: از ${old_price} به ${new_price}")

        # ۲. بررسی موجود شدن محصول
        if old_stock == 0 and new_stock > 0:
            alerts.append(f"🟢 **شارژ مجدد کالا**: تعداد {new_stock} عدد موجود شد.")

        # ۳. بررسی اتمام موجودی
        if old_stock > 0 and new_stock == 0:
            alerts.append("🔴 **اتمام موجودی!**")

        if alerts:
            message = "\n".join(alerts)
            return True, message

        return False, "هیچ تغییر حائز اهمیتی رخ نداده است."
