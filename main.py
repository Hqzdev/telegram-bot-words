#!/usr/bin/env python3
"""
Telegram Bot для опроса собственников земельных участков
"""

import asyncio
import logging
import nest_asyncio
from dotenv import load_dotenv
from telegram import Update
from bot.handlers import setup_handlers
from bot.bot_instance import initialize_bot
from bot.config import Config

# Применяем nest_asyncio для решения проблем с event loop
nest_asyncio.apply()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Главная функция запуска бота"""
    # Загружаем переменные окружения
    load_dotenv()
    
    # Инициализируем конфигурацию
    config = Config()
    
    # Инициализируем бота
    bot = initialize_bot()
    
    # Настраиваем обработчики
    setup_handlers(bot)
    
    # Запускаем бота
    logger.info("Запуск бота...")
    await bot.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
