#!/usr/bin/env python3
"""
Максимально простой бот для тестирования
"""

import asyncio
import logging
import os
import nest_asyncio
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

# Применяем nest_asyncio для решения проблем с event loop
nest_asyncio.apply()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update, context):
    """Простая команда start"""
    await update.message.reply_text("Бот работает! Это тестовое сообщение.")

async def main():
    """Главная функция"""
    # Загружаем переменные окружения
    load_dotenv()
    
    # Получаем токен напрямую
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        logger.error("TELEGRAM_TOKEN не найден в переменных окружения")
        return
    
    logger.info(f"Токен найден: {token[:10]}...{token[-4:]}")
    
    # Создаем бота
    application = Application.builder().token(token).build()
    
    # Добавляем обработчик
    application.add_handler(CommandHandler("start", start_command))
    
    # Запускаем бота
    logger.info("Запуск простого бота...")
    await application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
