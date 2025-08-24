"""
Конфигурация бота
"""

import os
from typing import Optional

class Config:
    """Класс для управления конфигурацией бота"""
    
    def __init__(self):
        self.telegram_token: str = self._get_required_env('TELEGRAM_TOKEN')
        self.google_sheets_id: str = self._get_required_env('GOOGLE_SHEETS_ID')
        self.google_credentials_json: str = self._get_required_env('GOOGLE_CREDENTIALS_JSON')
    
    def _get_required_env(self, key: str) -> str:
        """Получить обязательную переменную окружения"""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Не установлена обязательная переменная окружения: {key}")
        return value
    
    def _get_optional_env(self, key: str, default: str = "") -> str:
        """Получить необязательную переменную окружения"""
        return os.getenv(key, default)





