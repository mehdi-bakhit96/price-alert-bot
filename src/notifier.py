import json
from pathlib import Path
from datetime import datetime
from loguru import logger
import httpx
from src.config import settings

ALERTS_DIR = Path("data")
ALERTS_FILE = ALERTS_DIR / "alerts_history.json"

class Notifier:
    def __init__(self):
        ALERTS_DIR.mkdir(parents=True, exist_ok=True)
        if not ALERTS_FILE.exists():
            ALERTS_FILE.write_text("[]", encoding="utf-8")

    def _save_local_alert(self, alert_data: dict):
        """ذخیره محلی هشدارها جهت بررسی و گزارش‌گیری"""
        try:
            records = json.loads(ALERTS_FILE.read_text(encoding="utf-8"))
            records.append({
                "timestamp": datetime.now().isoformat(),
                **alert_data
            })
            ALERTS_FILE.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            logger.error(f"خطا در ثبت لاگ محلی هشدار: {e}")

    async def send_alert(self, title: str, message: str, meta: dict = None):
        """ارسال چندکاناله هشدار"""
        meta = meta or {}
        
        # ۱. چاپ فرمت‌شده در ترمینال (همیشه فعال و تضمینی)
        box = f"""
==================== [ PRICE ALERT DETECTED ] ====================
عنوان: {title}
پیام: {message}
زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
اطلاعات محصول: {meta}
==================================================================
"""
        logger.success(box)

        # ۲. ذخیره در تاریخچه محلی (فایل JSON)
        self._save_local_alert({"title": title, "message": message, "meta": meta})

        # ۳. ارسال به تلگرام (در صورت فعال بودن و وجود دسترسی شبکه)
        if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
            await self._send_telegram(f"🔔 *{title}*\n\n{message}")

        # ۴. ارسال به دیسکورد (در صورت فعال بودن و وجود دسترسی شبکه)
        if settings.DISCORD_WEBHOOK_URL:
            await self._send_discord(title, message)

    async def _send_telegram(self, text: str):
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(url, json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"})
                if resp.status_code == 200:
                    logger.info("هشدار به تلگرام با موفقیت ارسال شد.")
                else:
                    logger.warning(f"عدم موفقیت تلگرام: کد وضعیت {resp.status_code}")
        except Exception:
            logger.warning("ارتباط شبکه با تلگرام برقرار نشد. هشدار به صورت محلی ذخیره شد.")

    async def _send_discord(self, title: str, message: str):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                payload = {
                    "embeds": [{
                        "title": title,
                        "description": message,
                        "color": 0x00FF00
                    }]
                }
                resp = await client.post(settings.DISCORD_WEBHOOK_URL, json=payload)
                if resp.status_code in (200, 204):
                    logger.info("هشدار به دیسکورد با موفقیت ارسال شد.")
        except Exception:
            logger.warning("ارتباط شبکه با دیسکورد برقرار نشد. هشدار به صورت محلی ذخیره شد.")

notifier = Notifier()
