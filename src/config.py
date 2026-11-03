import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

class Settings:
    CHECK_INTERVAL_SECONDS: int = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))
    TARGET_API_URL: str = os.getenv("TARGET_API_URL", "https://dummyjson.com/products/1")
    PRICE_DROP_PERCENT_THRESHOLD: float = float(os.getenv("PRICE_DROP_PERCENT_THRESHOLD", "5.0"))
    
    TELEGRAM_BOT_TOKEN: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: str | None = os.getenv("TELEGRAM_CHAT_ID")
    DISCORD_WEBHOOK_URL: str | None = os.getenv("DISCORD_WEBHOOK_URL")

settings = Settings()
