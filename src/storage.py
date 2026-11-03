import json
import os
from typing import Optional, Dict, Any
from src.logger import logger

STATE_FILE = "storage_state.json"

class StateStorage:
    def __init__(self, filepath: str = STATE_FILE):
        self.filepath = filepath

    def get_last_state(self, product_id: int) -> Optional[Dict[str, Any]]:
        if not os.path.exists(self.filepath):
            return None
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(str(product_id))
        except Exception as e:
            logger.warning(f"عدم موفقیت در خواندن فایل استیت: {e}")
            return None

    def save_state(self, product_id: int, state_data: Dict[str, Any]) -> None:
        all_data = {}
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    all_data = json.load(f)
            except Exception:
                all_data = {}

        all_data[str(product_id)] = state_data
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
