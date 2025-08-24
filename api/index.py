#!/usr/bin/env python3
"""
Vercel API endpoint для Telegram Bot
"""

import asyncio
import json
import logging
import sys
import os
from http.server import BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application

# Добавляем путь к модулям бота
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.handlers import setup_handlers
from bot.config import Config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальные переменные для бота
application = None

def initialize_bot_globally():
    """Инициализация бота глобально"""
    global application
    
    if application is None:
        # Загружаем переменные окружения
        from dotenv import load_dotenv
        load_dotenv()
        
        # Инициализируем конфигурацию
        config = Config()
        
        # Инициализируем приложение
        application = Application.builder().token(config.telegram_token).build()
        
        # Настраиваем обработчики
        setup_handlers(application)
        
        logger.info("Бот инициализирован для Vercel")

def handler(request, context):
    """Основная функция для Vercel serverless"""
    try:
        # Инициализируем бота если еще не инициализирован
        initialize_bot_globally()
        
        # Получаем метод запроса
        method = request.get('method', 'GET')
        
        if method == 'POST':
            # Получаем тело запроса
            body = request.get('body', '{}')
            
            # Парсим JSON
            update_data = json.loads(body)
            update = Update.de_json(update_data, application.bot)
            
            # Обрабатываем обновление
            asyncio.run(application.process_update(update))
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'ok'})
            }
        
        elif method == 'GET':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'Bot is running'})
            }
        
        else:
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
