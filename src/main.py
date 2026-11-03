import asyncio
import signal
from src.config import settings
from src.logger import logger
from src.tracker import ProductTracker
from src.storage import StateStorage
from src.alert_logic import AlertEngine
from src.notifier import Notifier

is_running = True

def handle_exit(sig, frame):
    global is_running
    logger.info("درخواست توقف برنامه دریافت شد...")
    is_running = False

async def run_pipeline(tracker: ProductTracker, storage: StateStorage):
    logger.info("در حال بررسی وضعیت جدید محصول...")
    current_data = await tracker.fetch_product_data()
    if not current_data:
        logger.warning("دیتایی دریافت نشد؛ رد شدن از این نوبت.")
        return

    product_id = current_data["id"]
    prev_data = storage.get_last_state(product_id)

    should_alert, reason = AlertEngine.evaluate(
        current=current_data,
        previous=prev_data,
        drop_threshold_percent=settings.PRICE_DROP_PERCENT_THRESHOLD
    )

    if should_alert:
        logger.warning(f"🚨 شرط هشدار فعال شد برای کالا {product_id}: {reason}")
        msg = (
            f"📢 **هشدار تغییر وضعیت محصول**\n"
            f"📦 کالا: `{current_data['title']}`\n"
            f"💵 قیمت فعلی: `${current_data['price']}`\n"
            f"📊 موجودی: `{current_data['stock']}`\n\n"
            f"{reason}"
        )
        await Notifier.send_telegram(msg)
        await Notifier.send_discord(msg)
    else:
        logger.info(f"وضعیت بررسی شد: {reason}")

    # به روز رسانی آخرین وضعیت
    storage.save_state(product_id, current_data)

async def main():
    logger.info("🚀 ربات مانیتورینگ قیمت و موجودی آغاز به کار کرد.")
    tracker = ProductTracker()
    storage = StateStorage()

    while is_running:
        await run_pipeline(tracker, storage)
        logger.info(f"خواب به مدت {settings.CHECK_INTERVAL_SECONDS} ثانیه...")
        await asyncio.sleep(settings.CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    asyncio.run(main())
