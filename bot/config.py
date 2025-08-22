"""
Конфигурация бота
"""

import os
import json
from typing import Optional

class Config:
    """Класс для управления конфигурацией бота"""
    
    def __init__(self):
        self.bot_token: str = self._get_required_env('BOT_TOKEN')
        self.google_sheets_id: str = self._get_required_env('GOOGLE_SHEETS_ID')
        self.google_credentials_file: Optional[str] = self._get_optional_env('GOOGLE_CREDENTIALS_FILE')
        self.google_credentials_json: Optional[str] = self._get_optional_env('GOOGLE_CREDENTIALS_JSON')
    
    def _get_required_env(self, key: str) -> str:
        """Получить обязательную переменную окружения"""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Не установлена обязательная переменная окружения: {key}")
        return value
    
    def _get_optional_env(self, key: str, default: str = "") -> str:
        """Получить необязательную переменную окружения"""
        return os.getenv(key, default)
    
    def get_google_credentials(self) -> dict:
        """Получить учетные данные Google в виде словаря"""
        if self.google_credentials_json:
            # Если есть JSON в переменной окружения
            return json.loads(self.google_credentials_json)
        elif self.google_credentials_file and os.path.exists(self.google_credentials_file):
            # Если есть файл с учетными данными
            with open(self.google_credentials_file, 'r') as f:
                return json.load(f)
        else:
            raise ValueError("Не найдены учетные данные Google. Установите GOOGLE_CREDENTIALS_JSON или GOOGLE_CREDENTIALS_FILE")
