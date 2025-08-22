#!/usr/bin/env python3
"""
Простой тест бота
"""

import asyncio
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from bot.config import Config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update, context):
    """Простая команда start для тестирования"""
    await update.message.reply_text("Бот работает! Это тестовое сообщение.")

async def main():
    """Главная функция"""
    # Загружаем переменные окружения
    load_dotenv()
    
    # Создаем конфигурацию
    config = Config()
    
    # Создаем бота
    application = Application.builder().token(config.telegram_token).build()
    
    # Добавляем обработчик
    application.add_handler(CommandHandler("start", start_command))
    
    # Запускаем бота
    logger.info("Запуск тестового бота...")
    await application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
