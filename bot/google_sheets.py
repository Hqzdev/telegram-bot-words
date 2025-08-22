"""
Модуль для работы с Google Sheets API
"""

import os
from typing import List, Dict, Any
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)

class GoogleSheetsManager:
    """Менеджер для работы с Google Sheets"""
    
    def __init__(self, credentials_file: str, spreadsheet_id: str):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.service = self._create_service()
    
    def _create_service(self):
        """Создать сервис Google Sheets"""
        try:
            # Области доступа
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            
            # Загружаем учетные данные
            credentials = Credentials.from_service_account_file(
                self.credentials_file, scopes=scopes
            )
            
            # Создаем сервис
            service = build('sheets', 'v4', credentials=credentials)
            return service
            
        except Exception as e:
            logger.error(f"Ошибка при создании сервиса Google Sheets: {e}")
            raise
    
    def initialize_sheet(self):
        """Инициализировать таблицу с заголовками"""
        try:
            # Заголовки таблицы
            headers = [['Вопросы', 'Ответы']]
            
            # Записываем заголовки
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='A1:B1',
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()
            
            logger.info("Таблица инициализирована с заголовками")
            
        except HttpError as e:
            logger.error(f"Ошибка при инициализации таблицы: {e}")
            raise
    
    def append_survey_data(self, survey_data: List[List[str]]):
        """Добавить данные опроса в таблицу"""
        try:
            # Добавляем данные
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range='A:B',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': survey_data}
            ).execute()
            
            # Добавляем пустую строку после анкеты
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range='A:B',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': [['', '']]}
            ).execute()
            
            logger.info(f"Добавлены данные опроса: {len(survey_data)} строк")
            
        except HttpError as e:
            logger.error(f"Ошибка при добавлении данных в таблицу: {e}")
            raise
    
    def get_last_row(self) -> int:
        """Получить номер последней строки с данными"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range='A:A'
            ).execute()
            
            values = result.get('values', [])
            return len(values)
            
        except HttpError as e:
            logger.error(f"Ошибка при получении последней строки: {e}")
            return 1
    
    def test_connection(self) -> bool:
        """Проверить подключение к Google Sheets"""
        try:
            # Пытаемся получить информацию о таблице
            self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            return True
        except HttpError as e:
            logger.error(f"Ошибка подключения к Google Sheets: {e}")
            return False
