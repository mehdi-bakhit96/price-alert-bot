from typing import Optional, Dict, Any
import httpx
from src.logger import logger
from src.config import settings

class ProductTracker:
    def __init__(self, api_url: Optional[str] = None):
        self.api_url = api_url or settings.TARGET_API_URL

    async def fetch_product_data(self) -> Optional[Dict[str, Any]]:
        """
        اطلاعات محصول شامل قیمت و موجودی را استخراج می‌کند.
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.api_url)
                response.raise_for_status()
                data = response.json()
                
                logger.debug(f"داده خام محصول دریافت شد: ID {data.get('id')}")
                return {
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "price": float(data.get("price", 0.0)),
                    "stock": int(data.get("stock", 0)),
                    "availability": data.get("availabilityStatus", "Unknown")
                }
        except httpx.HTTPStatusError as exc:
            logger.error(f"خطای وضعیت HTTP: {exc.response.status_code} برای {exc.request.url}")
        except httpx.RequestError as exc:
            logger.error(f"خطای ارتباط شبکه: {exc}")
        except Exception as exc:
            logger.exception(f"خطای پیش‌بینی نشده در فچ دیتا: {exc}")
            
        return None
